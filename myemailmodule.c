#include <python.h>
#include <wchar.h>

static PyObject*
myemail_makestr( PyObject* self, PyObject* args )
{
	char* str;
	int len;
	if ( !PyArg_ParseTuple( args, "uuuu", &sp, &addr, &time, &state ) )
		return NULL;
	wchar_t a[100] = "판매장소: ";
	wchar_t b[100] = "주소: ";
	wchar_t c[100] = "입고시간: ";
	wchar_t d[100] = "재고상태: ";

	wcscat( a, sp );
	wcscat( b, addr );
	wcscat( c, time );
	wcscat( d, state );

	return Py_BuildValue( "uuuu", a, b, c, d );
}

static PyMethodDef myemailMethods[] = {
	{"makestr", myemail_makestr, METH_VARARGS, "make information string."},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef myemailmodule = {
	PyModuleDef_HEAD_INIT,
	"myemail",
	"This is for google email.",
	-1, myemailMethods
};

PyMODINIT_FUNC
PyInit_myemail( void )
{
	return PyModule_Create( &myemailmodule );
}