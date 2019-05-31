import arcpy, os, sys

enterprise_sde = r'Database Connections\Prod_GIS_Halifax.sde'

domains = arcpy.da.ListDomains(enterprise_sde)

domain_names = [x.name for x in domains]
domains_dict = dict(zip(domain_names, domains))
coded_values = [x.codedValues for x in domains]


def get_domains(workspace):
    return arcpy.da.ListComains(workspace)


def get_codedvalues(domain_obj):
    if domain_obj.domainType == 'CodedValue':
        result = domain_obj.codedValues
        print "Coded values for Domain '{}':\n\t {}".format(domain_obj.name, domain_obj.codedValues)
        return result


print get_codedvalues(domains[1])


def get_domaininfo(featureclass):

    domains = arcpy.da.ListDomains(enterprise_sde)
    domain_names_all = [x.name for x in domains]
    domains_dict = dict(zip(domain_names_all, domains))

    fieldnames_wdomains = [field.name for field in arcpy.ListFields(featureclass) if field.domain != ""]
    fields_wdomains = [field for field in arcpy.ListFields(featureclass) if field.domain != ""]
    domain_names = [field.domain for field in fields_wdomains]

    coded_values = [domains_dict[name].codedValues for name in domain_names]

    fields_domains = dict(zip(fieldnames_wdomains, domain_names))
    domains_codedvalues = dict(zip(domain_names, coded_values))
    master_dict = dict(zip(fieldnames_wdomains, zip(domain_names, coded_values)))

    print "\nFields & Domains\n", fields_domains
    print "\nDomains & Coded Values\n", domains_codedvalues

    print "\n\nALL\n", master_dict
    for item in master_dict.items():
        print item

    return domains, coded_values


# get_domaininfo(r'Database Connections\Prod_GIS_Halifax.sde\SDEADM.LND_hrm_parcel_parks\SDEADM.LND_hrm_park')


