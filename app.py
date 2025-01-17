import streamlit as st

st.write("""
# From ERT to GIS 🚀
""")

with st.form('computation'):
    uploaded_file = st.file_uploader('Upload raw data from sensors (*.dat)')
    lat0 = st.number_input("Start point latitude", value=-13.711450057818931, step=1e-13, format="%.13f")
    lon0 = st.number_input("Start point longitude", value=48.485899385521066, step=1e-13, format="%.13f")
    lat1 = st.number_input("End point latitude", value=-13.711937336454291, step=1e-13, format="%.13f")
    lon1 = st.number_input("End point longitude", value=48.4856177535745, step=1e-13, format="%.13f")
    water_res_thres = st.number_input("Choose a resistivity max threshold for water", value=200)
    submit = st.form_submit_button('Transform ERT to GeoJSON')

if submit and uploaded_file is not None:
    st.write("## Step 1 : Inversion Process")
    import pygimli as pg
    from pygimli.physics import ert
    from matplotlib import pyplot as plt
    from io import StringIO

    with open("tmp/ert.dat", "wb") as tmp:
        tmp.write(uploaded_file.getvalue())

    data = ert.load("tmp/ert.dat")
    st.write("### File Description")
    st.write(data)
    data['k'] = ert.createGeometricFactors(data, numerical=True)
    mgr = ert.ERTManager(data)
    ax,cbar = mgr.showData()
    st.write("### Data from sensors")
    st.pyplot(ax.figure)
    data['err'] = ert.estimateError(data, relativeError=0.03, absoluteUError=5e-5)
    ax, cbar = ert.show(data, data['err']*100)
    st.write("### Errors")
    st.pyplot(ax.figure)

    with st.spinner(text='Performing Inversion...'):
        mod = mgr.invert(data, lam=10, verbose=True,paraDX=3, paraMaxCellSize=10, paraDepth=20, quality=33.6)
        ax, cbar = mgr.showResult()
        st.write("### Inversion Result")
        st.pyplot(ax.figure)
        mgr.saveResult("tmp")

    st.write("## Step 2 : Thresholding & getting coordinates")
    import numpy as np
    import pyvista as pv

    with st.spinner("Thresholding water..."):
        st.write("### Thresholded water")
        mesh = pv.read("tmp/ERTManager/resistivity.vtk")
        x,y,z = np.insert(np.delete(mesh.cell_centers().points, 2, axis=1), 2, mesh['Resistivity'], axis=1).transpose()
        z = np.array([ 0 if val < water_res_thres else 1 for val in z ])
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111)
        sc = ax.scatter(x,y, c=z, cmap='magma', marker='o')
        cbar = plt.colorbar(sc, ax=ax, shrink=0.5, aspect=5)
        cbar.set_label('Binary Representation (0 = Water, 1 = Non Water)')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Thresholded water')
        st.pyplot(fig)

    import pandas as pd
    from geographiclib.geodesic import Geodesic
    from geopy.distance import great_circle
    from geopy.point import Point
    from geopy import distance as geopy_distance

    pd.set_option("display.precision", 13)
    with st.spinner("Getting EPSG:4326 coordinates..."):
        st.write("### Coordinates")
        _mul = np.array([ np.NaN if val == 1 else 1 for val in z ])
        df = pd.DataFrame(np.column_stack((x*_mul,y*_mul)))
        df = df.loc[df[0].notna()].set_axis(['X', 'depth'], axis=1)
        P0 = Point(lat0, lon0)
        P1 = Point(lat1, lon1)

        def get_bearing(lat1, lat2, long1, long2):
            brng = Geodesic.WGS84.Inverse(lat1, long1, lat2, long2)['azi1']
            return brng

        bearing = get_bearing(lat0, lat1, lon0, lon1)
        print(f"Bearing from P0 to P1: {bearing} degrees")

        def append_coords(data):
            new_point = geopy_distance.distance(meters=data).destination(P0, bearing)
            return [new_point.latitude, new_point.longitude]

        new_df = pd.concat([df, df['X'].apply(append_coords)], axis=1).set_axis(['X', 'depth', 'lat_lon'], axis=1)
        new_df[['lat', 'lon']] = pd.DataFrame(new_df['lat_lon'].tolist(), index=df.index)
        new_df.drop(columns=['lat_lon'], inplace=True)
        st.dataframe(new_df, column_config={"lat": st.column_config.NumberColumn(format="%.13f"), "lon": st.column_config.NumberColumn(format="%.13f")})

        import json
        def to_geojson(df):
            def to_feature(df_line):
                return {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [df_line['lon'], df_line['lat']]
                    },
                    "properties": {
                        "depth": df_line['depth']
                    }
                }
            geo_df = df.apply(to_feature, axis=1)
            return json.dumps({
                "type": "FeatureCollection",
                "features": geo_df.to_numpy().tolist()
            })
        out_geojson = to_geojson(new_df)
        st.map(new_df, size=5)
        @st.experimental_fragment()
        def down_geojson ():
            st.download_button("Download as GeoJSON", data=out_geojson, file_name="water_points.json", mime="application/json")
        down_geojson()
