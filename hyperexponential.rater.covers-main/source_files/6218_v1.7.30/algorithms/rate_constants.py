# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers          = 1
benchmark_lr        = 0.7
default_num_rows    = 15    #used for claims > cat exhibit
default_num_years   = 15
dum_large_int       = 1e9
dum_nil_int         = 0
dum_old_date        = 19700101  
dum_new_date        = 1
dum_large_neg       = -999999


# used for exposure summary exhibits
year_built_breaks = [1919, 1939, 1959, 1979, 1995, 2001]
year_built_labels = ["<1920", "1920-1939", "1940-1959", "1960-1979", "1980-1995", "1996-2001", ">2002"]
year_built_bins = [year_built_breaks, year_built_labels]

num_floors_breaks = [1, 3, 7, 14]
num_floors_labels = ["1", "2-3", "4-7", "8-14", "15+"]
num_floors_bins = [num_floors_breaks, num_floors_labels]
