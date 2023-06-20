# test DP
library(sf)
library(readr)
library(raster)
library(mapview)

MIN_LNG<- -8.736818202921592
MIN_LAT <- 41.04562647469636
MAX_LNG <- -8.441249454672185
MAX_LAT <- 41.27284371515265


# transform bounding box from 4326 to 3035
pts <- matrix(c(MIN_LNG, MIN_LAT, MIN_LNG, MAX_LAT, MAX_LNG, 
                MAX_LAT, MAX_LNG, MIN_LAT, MIN_LNG, MIN_LAT), ncol=2, byrow=TRUE)
polygon_ext <- st_polygon(list(pts)) |> st_sfc(crs=4326) |> st_transform(3035)
extent <- st_as_sf(polygon_ext)|> raster::extent()
resolution <- 618

raster_template <- raster(crs= "+init=epsg:3035", 
                               resolution=resolution,
                               ext=extent,
                               vals=0) 

mapview(raster_template)

df <- read_csv("/Users/alexandra/Documents/GitHub/synth_data_evaluation/data/synthetic/dplocPORTO/porto_output_cell500_epsNone_mcmc_100_iter0_3035.csv")
df <- st_as_sf(df, coords = c("lng", "lat"))
df_raster <- rasterize(df, raster_template, field=1, fun="sum")

df_thres95 <- read_csv("/Users/alexandra/Documents/GitHub/synth_data_evaluation/data/synthetic/dplocPORTO/porto_output_cell500_epsNone_mcmc_100_iter0_thres95.csv")
df_thres95 <- st_as_sf(df_thres95, coords = c("lng", "lat"))
st_crs(df_thres95) <- 4326
df_thres95 <- df_thres95 |> st_transform(3035)
df_thres95$count <- 1

df_raster_thres95 <- rasterize(df_thres95, raster_template, field=1, fun="sum")
#df_raster_thres95_300 <- rasterize(df_thres95, raster_template, field=1, fun="sum")

mapview(df_raster)+
mapview(df_raster_thres95) + 
mapview(lines[1,], color="red") + 
mapview(lines[900,], color="blue") +
mapview(lines[1000,], color="green") 
#mapview(df_raster_thres95_300)


lines <- read_sf("/Users/alexandra/Documents/GitHub/synth_data_evaluation/data/synthetic/dplocPORTO/porto_output_cell500_epsNone_mcmc_100_iter0.geojson")[1:1000,]

mapview(df_raster) + mapview(lines[1:100,])


raster::writeRaster(df_raster, "/Users/alexandra/Documents/GitHub/synth_data_evaluation/data/synthetic/dplocPORTO/aggregated_points_porto.tif")
