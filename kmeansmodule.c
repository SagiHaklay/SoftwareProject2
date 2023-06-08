#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "kmeans.h"

static PyObject* fit(PyObject* self, PyObject* args)
{
    PyObject *lstPoints, *lstCentroids, *point, *item, *result;
    int k, iter, n, plength, i, j;
    double **datapoints, **centroids, num;
    if (!PyArg_ParseTuple(args, "OOi", &lstPoints, &lstCentroids, &iter)) {
        return NULL;
    }

    n = PyObject_Length(lstPoints);
    if (n < 0) {
        return NULL;
    }
    datapoints = (double **)calloc(n, sizeof(double *));
    if (datapoints == NULL) {
        printf("Memory allocation failed!\n");
        return NULL;
    }
    point = PyList_GetItem(lstPoints, 0);
    plength = PyObject_Length(point);
    for (i = 0; i < n; i++) {
        point = PyList_GetItem(lstPoints, i);
        datapoints[i] = (double *)calloc(plength, sizeof(double));
        if (datapoints[i] == NULL) {
            printf("Memory allocation failed!\n");
            return NULL;
        }
        for (j = 0; j < plength; j++) {
            item = PyList_GetItem(point, j);
            num = PyFloat_AsDouble(item);
            datapoints[i][j] = num;
        }
    }
    k = PyObject_Length(lstCentroids);
    if (k < 0) {
        return NULL;
    }
    centroids = (double **)calloc(n, sizeof(double *));
    if (centroids == NULL) {
        printf("Memory allocation failed!\n");
        return NULL;
    }
    for (i = 0; i < k; i++) {
        point = PyList_GetItem(lstCentroids, i);
        centroids[i] = (double *)calloc(plength, sizeof(double));
        if (centroids[i] == NULL) {
            printf("Memory allocation failed!\n");
            return NULL;
        }
        for (j = 0; j < plength; j++) {
            item = PyList_GetItem(point, j);
            num = PyFloat_AsDouble(item);
            centroids[i][j] = num;
        }
    }

    centroids = kmeans(datapoints, centroids, n, plength, k, iter);
    result = PyList_New(k);
    for (i = 0; i < k; i++) {
        point = PyList_New(plength);
        for (j = 0; j < plength; j++) {
            item = PyFloat_FromDouble(centroids[i][j]);
            PyList_SetItem(point, j, item);
        }
        PyList_SetItem(result, i, point);
        free(centroids[i]);
    }
    for (i = 0; i < n; i++) {
        free(datapoints[i]);
    }
    free(datapoints);
    free(centroids);
    return result;
}

static PyMethodDef kmeansMethods[] = {
    {"fit",
    (PyCFunction)fit,
    METH_VARARGS,
    PyDoc_STR("Runs k-means on a list of datapoints with the chosen initial centroids and max iterations. Args: datapoints - a list of float lists, initial centroids - a list of float lists, max iteration - integer")},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef kmeansModule = {
    PyModuleDef_HEAD_INIT,
    "mykmeanssp",
    NULL,
    -1,
    kmeansMethods
};

PyMODINIT_FUNC PyInit_mykmeanssp(void)
{
    PyObject *m;
    m = PyModule_Create(&kmeansModule);
    if (!m) {
        return NULL;
    }
    return m;
}