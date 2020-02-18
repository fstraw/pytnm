from arcpy import da


def create_impact_narrative(receivers):
    """Generate narrative for report based on receiver database
    
    Arguments:
        receivers {String} -- Path to feature class
    """

    flds = ('du', 'ex_snd', 'nobld_snd', 'bld_snd', 'nac_cat')
    sensitive_query = "nac_cat IN ('A', 'B', 'C', 'D', 'E')"
    sensitive_receivers = [row for row in da.SearchCursor(receivers, flds, sensitive_query)]
    sensitive_receivers_count = len(sensitive_receivers)
    sensitive_receivers_du_count = sum([row[0] for row in sensitive_receivers])
    sensitive_receivers_average_build = round(sum([row[3] - row[1] for row in sensitive_receivers]) / sensitive_receivers_count, 1)
    existing_minimum = min([row[1] for row in sensitive_receivers])
    existing_maximum = max([row[1] for row in sensitive_receivers])
    no_build_minimum = min([row[2] for row in sensitive_receivers])
    no_build_maximum = max([row[2] for row in sensitive_receivers])
    build_minimum = min([row[3] for row in sensitive_receivers])
    build_maximum = max([row[3] for row in sensitive_receivers])
    build_b_nac_impacts = [row[0] for row in sensitive_receivers if (row[4] == 'B' and row[3] >= 66)]
    build_c_nac_impacts = [row[0] for row in sensitive_receivers if (row[4] == 'C' and row[3] >= 66)]
    build_d_nac_impacts = [row[0] for row in sensitive_receivers if (row[4] == 'D' and row[3] >= 51)]
    build_e_nac_impacts = [row[0] for row in sensitive_receivers if (row[4] == 'E' and row[3] >= 71)]
    build_b_nac_impacted = len(build_b_nac_impacts)
    build_c_nac_impacted = len(build_c_nac_impacts)
    build_d_nac_impacted = len(build_d_nac_impacts)
    build_e_nac_impacted = len(build_e_nac_impacts)
    build_b_nac_impacted_du = sum(build_b_nac_impacts)
    build_c_nac_impacted_du = sum(build_c_nac_impacts)
    build_d_nac_impacted_du = sum(build_d_nac_impacts)
    build_e_nac_impacted_du = sum(build_e_nac_impacts)
    build_nac_impacted_receivers = sum((build_b_nac_impacted, build_c_nac_impacted, build_d_nac_impacted, build_e_nac_impacted))
    build_nac_impacted_receptors = sum((build_b_nac_impacted_du, build_c_nac_impacted_du, build_d_nac_impacted_du, build_e_nac_impacted_du))
    narrative = f"A total of {sensitive_receivers_count} receivers representing {sensitive_receivers_du_count} receptors were analyzed in the NSR."
    narrative += f" Noise is predicted to change by an average of {sensitive_receivers_average_build} dBA under the Build Alternative."
    narrative += f" Existing noise levels range from {existing_minimum} to {existing_maximum} dBA."
    narrative += f" No Build noise levels would range from {no_build_minimum} to {no_build_maximum} dBA."
    narrative += f" Build noise levels would range from {build_minimum} to {build_maximum} dBA."
    narrative += f" A total of {build_nac_impacted_receivers} receivers representing {build_nac_impacted_receptors} receptors would be impacted under the Build Alternative."
    return narrative

if __name__ == '__main__':
    fc = r'C:\Users\brbatt\Documents\!Noise\I10Pensacola\GIS\DATA\receiver.shp'
    print(create_impact_narrative(fc))