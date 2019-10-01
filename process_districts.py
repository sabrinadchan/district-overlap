import geopandas as gpd
import networkx as nx
import argparse
import subprocess

def main(in_fn, district, out_fn):
	gdf = gpd.read_file(in_fn)
	if district not in gdf.columns:
	  raise Exception("{} is not an attribute in the geospatial data.".format(district))
	gdf.rename(columns={district: "district"}, inplace=True) 

	adjacency = set()
	for d, g in zip(gdf.district, gdf.geometry):
	  neighbors = gdf.loc[gdf.geometry.touches(g), "district"].tolist()
	  for n in neighbors:
	  	adjacency.add((d, n))

	G = nx.Graph()
	G.add_edges_from(adjacency)

	coloring = nx.coloring.greedy_color(G, strategy='smallest_last')
	gdf["c"] = gdf.district.map(coloring)

	use_cols = ["district", "c", "geometry"]
	gdf[use_cols].to_file(out_fn, driver="TopoJSON")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("input", help="read file path")
	parser.add_argument("district", help="input file district name attribute")
	parser.add_argument("output", help="write file path")
	args = parser.parse_args()
	main(args.input, args.district, args.output)
