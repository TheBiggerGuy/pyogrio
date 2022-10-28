from pyogrio._ogr cimport *


cdef class ManagedOrgOGRFeature:
    cdef OGRFeatureH _ogr_feature

    @staticmethod
    cdef ManagedOrgOGRFeature from_ptr(OGRFeatureH ogr_feature)
