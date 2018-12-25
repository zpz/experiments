extern crate numpy;
use numpy::{PyArray1, IntoPyArray};

extern crate pyo3;
use pyo3::prelude::{pymodinit, Py, PyModule, PyResult, Python};

extern crate datex;
use datex::datex::{weekday, weekdays};


#[pymodinit(version01)]
fn version01(_py: Python, m: &PyModule) -> PyResult<()> {

    #[pyfn(m, "weekday")]
    fn weekday_py(_py: Python, x: i64) -> i64 {
        weekday(x)
    }

    #[pyfn(m, "weekdays")]
    fn weekdays_py(_py: Python, x: &PyArray1<i64>) -> Py<PyArray1<i64>> {
        weekdays(x.as_array()).into_pyarray(_py).to_owned()
    }

    Ok(())
}