from django.shortcuts import render
import folium
from folium.plugins import AntPath
from scgraph.geographs.marnet import marnet_geograph

def input_view(request):
    return render(request, 'input.html')

def calculate_route(request):
    if request.method == 'POST':
        origin_lat = float(request.POST.get('origin_lat'))
        origin_lng = float(request.POST.get('origin_lng'))
        dest_lat = float(request.POST.get('dest_lat'))
        dest_lng = float(request.POST.get('dest_lng'))

        # Get the shortest path between the provided points
        output = marnet_geograph.get_shortest_path(
            origin_node={"latitude": origin_lat, "longitude": origin_lng},
            destination_node={"latitude": dest_lat, "longitude": dest_lng}
        )

        # Create a map centered at the first location
        map_center = [output['coordinate_path'][0]['latitude'], output['coordinate_path'][0]['longitude']]
        mymap = folium.Map(location=map_center, zoom_start=5)

        # Create a line with arrows indicating the direction of the path
        path_points = [(point['latitude'], point['longitude']) for point in output['coordinate_path']]
        AntPath(locations=path_points, use_arrows=True, color='green').add_to(mymap)

        # Convert the map to HTML
        map_html = mymap._repr_html_()

        # Pass the map HTML to the template context
        context = {
            'map': map_html
        }

        # Render the template with the context
        return render(request, 'map.html', context)
    else:
        # Handle GET request
        return render(request, 'input.html')
