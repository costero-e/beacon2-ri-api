
import './App.css';
import { Route, Routes } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import Individuals from './components/Individuals';
import Individuals2 from './components/Individual2';
import GenomicVariations from './components/GenomicVariations';
import Biosamples from './components/Biosamples';
import Runs from './components/Runs';
import Analyses from './components/Analyses';
import Cohorts from './components/Cohorts';
import Datasets from './components/Datasets'
import ErrorPage from './pages/ErrorPage';
import Navbar from './components/Navbar';
import Members from './components/Members';
import History from './components/History';
import SignInForm from './components/SignInForm';
import SignUpForm from './components/SignUpForm';
import ResultsDatasets from './components/ResultsDatasets';


function Layout() {

  const [error, setError] = useState(null)
  const [collectionType, setCollectionType] = useState(["Select", "Individuals", "Cohorts", "Datasets", "Biosamples", "Analyses", "Runs", "Variant"])
  const [collection, setCollection] = useState('')
  const [placeholder, setPlaceholder] = useState('')
  const [results, setResults] = useState(null)
  const [query, setQuery] = useState(null)
  const [exampleQ, setExampleQ] = useState([])
  const [showAdvSearch, setAdvSearch] = useState(false)


  const Add = collectionType.map(Add => Add)

  const handleAddrTypeChange = (e) => {

    setCollection(collectionType[e.target.value])
    setExampleQ([])

  }

  const handleAdvancedSearch = (e) => {
    setAdvSearch(true)
  }

  const handleBasicSearch = (e) => {
    setAdvSearch(false)
  }

  const handleExQueries = () => {
    if (collection === 'Individuals') {
      setExampleQ(['sex= male, ethnicity=White and Black Caribbean', 'sex=female,cardiomyopathy', 'ethnicity=NCIT:C16352,weight>50'])
    }
  }

  useEffect(() => {

    setResults(null)

    if (collection === 'Individuals') {
      setPlaceholder('key=value, key><=value, or filtering term comma-separated')
    } else if (collection === 'Biosamples') {
      setPlaceholder('key=value, key><=value, or filtering term comma-separated')
    } else if (collection === 'Cohorts') {
      setPlaceholder('Search for any cohort')
    } else if (collection === "Variant") {
      setPlaceholder('chr : pos ref > alt')
    } else if (collection === "Analyses") {
      setPlaceholder('chr : pos ref > alt')
    } else if (collection === "Runs") {
      setPlaceholder('chr : pos ref > alt')
    } else if (collection === 'Datasets') {
      setPlaceholder('Search for any cohort')
    } else {
      setPlaceholder('')
    }

  }, [collection])


  const onSubmit = async (event) => {
    event.preventDefault()

    try {
      if (query === '1' || query === '') {
        setQuery(null)
      }
      if (collection === 'Individuals') {
        setResults('Individuals')
      } else if (collection === 'Cohorts') {
        setResults('Cohorts')
      }


    } catch (error) {
      console.log(error)
      setError(error.response.data.errorMessage)
    }
  }

  function search(e) {
    setQuery(e.target.value)
    setResults(null)
  }

  return (
    <div className="container1">
      <a href="https://www.cineca-project.eu/">
        <img className="cinecaLogo" src="./CINECA_logo.png" alt='searchIcon'></img>
      </a>
      <nav className="navbar">
        <div className="container-fluid">
          <select className="form-select" aria-label="Default select example" onChange={e => { handleAddrTypeChange(e) }}>
            {
              Add.map((collection, key) => <option key={key} value={key}>{collection}
              </option>)
            }
          </select>
          <form className="d-flex" onSubmit={onSubmit}>
            <input className="formSearch" type="search" placeholder={placeholder} onChange={(e) => search(e)} aria-label="Search" />
            {!showAdvSearch && <button className="searchButton" type="submit"><img className="searchIcon" src="./magnifier.png" alt='searchIcon'></img></button>}
          </form>
        </div>
        {!showAdvSearch && <button className="advSearch" onClick={handleAdvancedSearch}>
          Advanced search
        </button>}
        {showAdvSearch && <form className='advSearchForm'>
          <div className='advSearchModule'>
            <label>SKIP</label>
            <input className="skipForm" type="number" autoComplete='on' placeholder={0} onChange={(e) => search(e)} aria-label="Search" />
            <label>LIMIT</label>
            <input className="limitForm" type="number" autoComplete='on' placeholder={10} onChange={(e) => search(e)} aria-label="Search" />
          </div>

          <div className='advSearchModule'>
            <label>Include Resultset Responses</label>
            <input className="limitForm" type="text" autoComplete='on' placeholder={""} onChange={(e) => search(e)} aria-label="Search" />
            <label>Similarity</label>
            <input className="limitForm" type="text" autoComplete='on' placeholder={""} onChange={(e) => search(e)} aria-label="Search" />
            <label>Include Descendant Terms</label>
            <input className="limitForm" type="text" autoComplete='on' placeholder={""} onChange={(e) => search(e)} aria-label="Search" />
          </div>
          <button className="searchButton2" type="submit"><img className="searchIcon" src="./magnifier.png" alt='searchIcon'></img></button>
        </form>}

      </nav>
      <div className="example">
        <button className="exampleQueries" onClick={handleExQueries}>Query Examples</button>
        <img className="bulbLogo" src="../light-bulb.png" alt='bulbIcon'></img>
        {exampleQ[0] && exampleQ.map((result) => {
          return (<div id='exampleQueries'>

            <button className="exampleQuery" onClick={() => { setPlaceholder(`${result}`); setQuery(`${result}`); setResults(null) }} >{result}</button>
          </div>)

        })}

      </div>
      {showAdvSearch && <button className='returnBasic' onClick={handleBasicSearch}>RETURN TO BASIC SEARCH</button>}

      <hr></hr>
      <div className="results">
        {results === null && <ResultsDatasets />}
        {results === 'Individuals' && <Individuals2 query={query} />}
      </div>
    </div>

  );
}

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path='/' element={<Layout />} />
        <Route path='/individuals' element={<Individuals />} />
        <Route path='/genomicVariations' element={<GenomicVariations />} />
        <Route path='/biosamples' element={<Biosamples />} />
        <Route path='/runs' element={<Runs />} />
        <Route path='/analyses' element={<Analyses />} />
        <Route path='/cohorts' element={<Cohorts />} />
        <Route path='/datasets' element={<Datasets />} />
        <Route path='members' element={<Members />} />
        <Route path='/history' element={<History />} />
        <Route path='/sign-up' element={<SignUpForm />} />
        <Route path="/sign-in" element={<SignInForm />} />
        <Route path="*" element={<ErrorPage />} />
      </Routes>
    </div>
  );
}



export default App;


