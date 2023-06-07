#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject* fit(PyObject* self, PyObject* args)
{

}

static PyMethodDef kmeansMethods[] = {
    {"fit",
    (PyCFunction)fit,
    METH_VARARGS,
    PyDoc_STR("")},
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