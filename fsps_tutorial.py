import fsps

# Initializes a simple stellar population with solar metallicity 
# of zero, since logzsol = log(z/z_sol) = 0.0 if z = z_sol
# Some dust, and Calzetti extinction curve
sp = fsps.StellarPopulation(compute_vega_mags=False, zcontinuous=1,
                            sfh=0, logzsol=0.0, dust_type=2, dust2=0.2)


