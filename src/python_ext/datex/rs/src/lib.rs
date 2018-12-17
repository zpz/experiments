#![feature(specialization)]
#![feature(custom_attribute)]

#[macro_use]

extern crate pyo3;
extern crate datex;
extern crate numpy;
extern crate ndarray;

use pyo3::prelude::*; //{Py, Python, pyfunction, pymodule, PyModule, PyResult};
use ndarray::{Array1};
use numpy::{PyArray1};

use datex::datex::weekday as weekday_;



#[pyfunction]
fn weekday(x: i64) -> i64 {
    weekday_(x)
}


#[pyfunction]
fn weekdays(x: &PyArray1<i64>) -> Py<PyArray1<i64>> {
    let mut out = Array1::<i64>::zeros(x.len());
    for (i, xx) in x.iter().enumerate() {
        out[i] = weekday(*xx);
    }
    let gil = pyo3::Python::acquire_gil();
    out.to_pyarray(gil.python())
}


#[pymodule]
fn version01(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_function!(weekday))?;
    m.add_wrapped(wrap_function!(weekdays))?;

    Ok(())
}

