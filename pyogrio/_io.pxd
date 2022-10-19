from libc.stdint cimport uint8_t

from pyogrio._ogr cimport *


cdef class ManagedOrgOGRFeature:
    cdef OGRFeatureH _ogr_feature

    cdef OGRGeometryH get_geometry_ref(self)

    cdef bytes geometry_as_wkb(self, uint8_t force_2d)

    @staticmethod
    cdef ManagedOrgOGRFeature from_ptr(OGRFeatureH ogr_feature)


cdef class OrgLayerIter:
    cdef OGRLayerH _ogr_layer
    cdef int _skip_features
    cdef int _num_features
    cdef int _i

    @staticmethod
    cdef OrgLayerIter from_ptr(OGRLayerH ogr_layer, int skip_features, int num_features)
