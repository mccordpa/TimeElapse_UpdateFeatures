"""
Updates fields when a certain period of time elapses. 
The below script is simply using dummy data. 
Once six days elapses between the Install Date and the Current Date,
the Fitting Type is changed to Expansion Joint.
"""

from arcgis.gis import GIS
import datetime

#!!! RESOURCE: https://community.esri.com/t5/arcgis-api-for-python-questions/updating-feature-layer-using-arcgis-api-for-python/td-p/777275
#!!! RESOURCE: https://developers.arcgis.com/python/samples/updating-features-in-a-feature-layer/
#!!! RESOURCE: https://developers.arcgis.com/python/guide/working-with-feature-layers-and-features/

gis = GIS(profile="ohm_ago")

print(gis.users.me.username)

# Feature Layer Collection Item to update
item = gis.content.get("acf88ccb26d546eebc5754b160a644fe")

# feature layer
# the feature layer instance is within the layers attribute of the Feature Layer Collection Item obtained above
fl = item.layers[0]

# feature set
# We want to read the attribute table of the feature layer. Querying the feature layer returns a Feature Set,
# which can display the attribute table.
fset = fl.query()

# feature layer in table format
# The Spatial Data Frame property is available to the Feature Set. This allows us to view the Features as a dataframe.
fset_rows = fset.sdf

# iterate through rows and update record if condition is met
today = datetime.datetime.today()
for index, row in fset_rows.iterrows():
    install_date = row["INSTALLDATE"]
    time_delta = today - install_date
    delta_days = time_delta.days

    if delta_days >= 6:
        print(f"updating {row['FACILITYID']}.... ")
        # Update feature 
        fset.features[index].attributes["FITTINGTYPE"] = "Expansion Joint"
        # The Feature Layer is updated when the edit_features() method is called on the Feature Layer object
        # The list of features from the Feature Set are passed to the Updates parameter.
        fl.edit_features(updates=fset.features)
        print(f"Updated fitting type on {row['FACILITYID']}.")
