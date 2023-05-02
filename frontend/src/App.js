import 'devextreme/dist/css/dx.light.css';

import './App.css';
import { Route, Routes } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
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
import FilteringTermsIndividuals from './components/FilteringTermsIndividuals';

import Select from 'react-select'

import { AuthContext } from './components/context/AuthContext';
import { useContext } from 'react';

import axios from "axios";

import ReactModal from 'react-modal';
import makeAnimated from 'react-select/animated';



function Layout() {

  const [error, setError] = useState(null)
  const [collectionType, setCollectionType] = useState(["Select collection", "Individuals", "Cohorts", "Datasets", "Biosamples", "Analyses", "Runs", "Variant"])
  const [collection, setCollection] = useState('')
  const [placeholder, setPlaceholder] = useState('')
  const [results, setResults] = useState(null)
  const [query, setQuery] = useState(null)
  const [exampleQ, setExampleQ] = useState([])
  const [showAdvSearch, setAdvSearch] = useState(false)
  const [showAlphanumValue, setAlphanumValue] = useState(false)
  const [resultSetType, setResultsetType] = useState(["Select", "HIT", "MISS", "NONE", "ALL"])
  const [resultSet, setResultset] = useState("HIT")

  const [cohorts, setShowCohorts] = useState(false)

  const [ID, setId] = useState("")
  const [operator, setOperator] = useState("")
  const [value, setValue] = useState("")

  const [popUp, setPopUp] = useState(false)

  const [descendantTermType, setDescendantTermType] = useState(["Select", "true", "false"])
  const [descendantTerm, setDescendantTerm] = useState("true")

  const [similarityType, setSimilarityType] = useState(["Select", "low", "medium", "high"])
  const [similarity, setSimilarity] = useState("Select")

  const [showFilteringTerms, setShowFilteringTerms] = useState(false)
  const [filteringTerms, setFilteringTerms] = useState(false)

  const { storeToken, refreshToken, getStoredToken, authenticateUser, setExpirationTime, setExpirationTimeRefresh } = useContext(AuthContext);

  const Add = collectionType.map(Add => Add)

  const Add2 = resultSetType.map(Add2 => Add2)

  const Add3 = descendantTermType.map(Add3 => Add3)

  const Add4 = similarityType.map(Add4 => Add4)

  const [isOpenModal1, setIsOpenModal1] = useState(false);
  const [isOpenModal2, setIsOpenModal2] = useState(false);

  const [showAlph, setShowAlph] = useState(false)
  const [showAdvButton, setShowAdvButton] = useState(false)

  const animatedComponents = makeAnimated();

  const [options, setOptions] = useState([
    { value: 'CINECA_synthetic_cohort_UK1', label: 'CINECA_synthetic_cohort_UK1' },
    { value: 'Fake cohort 1', label: 'Fake cohort 1' },
    { value: 'Fake cohort 2', label: 'Fake cohort 2' }
  ])

  const handleAddrTypeChange = (e) => {

    setCollection(collectionType[e.target.value])
    setExampleQ([])
    setFilteringTerms(false)
    setShowFilteringTerms(false)

  }

  const handleClick = (e) => {
    setCollectionType(["Select collection", "Individuals", "Cohorts", "Datasets", "Biosamples", "Analyses", "Runs", "Variant"])
    setCollection(collectionType[e.target.value])
  }

  const handleResultsetChanges = (e) => {
    setResultset(resultSetType[e.target.value])
  }

  const handleDescendantTermChanges = (e) => {
    setDescendantTerm(descendantTermType[e.target.value])
  }

  const handleSimilarityChanges = (e) => {

    setSimilarity(similarityType[e.target.value])
  }


  const handleAdvancedSearch = (e) => {
    setAdvSearch(true)
  }


  const handleIdChanges = (e) => {
    setId(e.target.value)
  }

  const handleOperatorChanges = (e) => {
    setOperator(e.target.value)

  }

  const handleValueChanges = (e) => {
    setValue(e.target.value)
  }

  const handleBasicSearch = (e) => {
    setAdvSearch(false)
  }

  const handleHelpModal1 = () => {
    setIsOpenModal1(true)
  }

  const handleCloseModal1 = () => {
    setIsOpenModal1(false)
  }

  const handleHelpModal2 = () => {
    setIsOpenModal2(true)
  }

  const handleCloseModal2 = () => {
    setIsOpenModal2(false)
  }

  const handleCloseModal3 = () => {
    setPopUp(false)
  }


  const handleFilteringTerms = async (e) => {

    console.log(collection)
    if (collection === 'Individuals') {

      try {

        let res = await axios.get("http://localhost:5050/api/individuals/filtering_terms?limit=0")
        setFilteringTerms(res)
        setResults(null)

      } catch (error) {
        console.log(error)
      }
    } else if (collection === 'Cohorts') {

      try {

        let res = await axios.get("http://localhost:5050/api/cohorts/filtering_terms?limit=0")
        setFilteringTerms(res)
        setResults(null)

      } catch (error) {
        console.log(error)
      }
    }


    setShowFilteringTerms(true)


  }

  const handleFilteringTermsAll = async (e) => {
  }

  const handleExQueries = () => {
    if (collection === 'Individuals') {
      setExampleQ(['sex= male, ethnicity=White and Black Caribbean', 'sex=female,cardiomyopathy', 'ethnicity=NCIT:C16352,LOINC:3141-9>50', 'NCIT:C42331'])
    }
  }

  const handleExQueriesAlphaNum = () => {

  }

  useEffect(() => {
    const token = getStoredToken()

    if (token === null) {
      const timer = setTimeout(() => setPopUp(true), 1000);
      setPopUp(false)
      return () => clearTimeout(timer);
    }

  }, [])

  useEffect(() => {

    setShowCohorts(false)
    setResults(null)

    if (collection === 'Individuals') {
      setPlaceholder('key=value, key><=value, or filtering term comma-separated')
      setShowAlph(true)
      setShowAdvButton(true)
    } else if (collection === 'Biosamples') {
      setPlaceholder('key=value, key><=value, or filtering term comma-separated')
    } else if (collection === 'Cohorts') {
      setShowCohorts(true)
      setShowAlph(false)
      setShowAdvButton(false)
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


    setCollectionType([`${collection}`])

    authenticateUser()

    setExampleQ([])



    setAdvSearch(false)
    setAlphanumValue(false)

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
      <div className='Modal1'>
        {popUp && <ReactModal
          isOpen={popUp}
          onRequestClose={handleCloseModal3}
          shouldCloseOnOverlayClick={true}
        >
          <button onClick={handleCloseModal3}><img className="closeLogo" src="./cancel.png" alt='cancelIcon'></img></button>

          <p>Please, bear in mind that you might have to log in to get information from some datasets.</p>

        </ReactModal>
        }
      </div>

      <button className="helpButton" onClick={handleHelpModal2}><img className="questionLogo2" src="./question.png" alt='questionIcon'></img><h5>Help for querying</h5></button>
      <nav className="navbar">
        <div className="container-fluid">
          <select className="form-select" aria-label="Default select example" onClick={handleClick} onChange={e => { handleAddrTypeChange(e) }}>
            {
              Add.map((collection, key) => <option key={key} value={key}>{collection}
              </option>)
            }
          </select>

          {cohorts === false &&
            <form className="d-flex" onSubmit={onSubmit}>
              <input className="formSearch" type="search" placeholder={placeholder} onChange={(e) => search(e)} aria-label="Search" />
              <button className="searchButton" type="submit"><img className="searchIcon" src="./magnifier.png" alt='searchIcon'></img></button>
            </form>}

          {cohorts &&

            <form className="d-flex2" onSubmit={onSubmit}>

              {results !== 'Cohorts' && <button className="searchButton2" type="submit"><img className="forwardIcon" src="./adelante.png" alt='searchIcon'></img></button>}
            </form>
          }
          {results === "Cohorts" && <Select
            closeMenuOnSelect={false}
            components={animatedComponents}
            defaultValue={[options[0]]}
            isMulti
            options={options}
          />}

        </div>

        <div className="additionalOptions">

          {!showAdvSearch && showAdvButton &&

            <div className='AdvSearchDiv'>
              <button className="advSearch" onClick={handleAdvancedSearch}>
                Advanced search
              </button>
            </div>}

          <div className="example">
            {cohorts === false && collection !== '' &&
              <div className="bulbExample">
                <button className="exampleQueries" onClick={handleExQueries}>Query Examples</button>
                <img className="bulbLogo" src="../light-bulb.png" alt='bulbIcon'></img>
                <div>
                  {exampleQ[0] && exampleQ.map((result) => {

                    return (<div id='exampleQueries'>


                      <button className="exampleQuery" onClick={() => { setPlaceholder(`${result}`); setQuery(`${result}`); setResults(null) }}  >{result}</button>
                    </div>)

                  })}
                </div>
              </div>
            }

            {collection !== '' && <button className="filters" onClick={handleFilteringTerms}>
              Filtering Terms
            </button>}

            {collection === '' && <button className="filters" onClick={handleFilteringTermsAll}>
              Filtering terms of all collections
            </button>}

          </div>


        </div>
        {showAlph && <div className='alphanumContainer'>
          <hr></hr>
          <h2>Alphanumerical and numerical queries</h2>
          <button className="helpButton" onClick={handleHelpModal1}><img className="questionLogo" src="./question.png" alt='questionIcon'></img></button>

          <div className='alphanumContainer2'>
            <label><h2>ID</h2></label>
            <input className="IdForm" type="text" autoComplete='on' placeholder={"write the ID"} onChange={(e) => handleIdChanges(e)} aria-label="ID" />


            <div id="operator">
              <h2>OPERATOR</h2>
              <input className="operator"></input>

            </div>

            <label id="value"><h2>Value</h2></label>
            <input className="ValueForm" type="text" autoComplete='on' placeholder={"free text/ value"} onChange={(e) => handleValueChanges(e)} aria-label="Value" />
          </div>
          <div className="exampleQueriesAlph">
            <button className="exampleQueries" onClick={handleExQueriesAlphaNum}>Query Examples</button>
          </div>
        </div>} <hr></hr>

        <form className='advSearchForm' onSubmit={onSubmit}>

          {showAdvSearch && <div className='advSearchModule' >

            <button className="helpButton2" onClick={handleHelpModal1}><img className="questionLogo" src="./question.png" alt='questionIcon'></img></button>
            <div className='resultset'>



              <div className="advSearch-module">

                <label><h2>Include Resultset Responses</h2></label>
                <select className="form-select2" aria-label="" onChange={(e) => handleResultsetChanges(e)}>
                  {
                    Add2.map((resultSet, key) => <option key={key} value={key}>{resultSet}
                    </option>)
                  }
                </select>
              </div>

              <div className="advSearch-module">
                <label><h2>Similarity</h2></label>
                <select className="form-select2" aria-label="" onChange={e => { handleSimilarityChanges(e) }}>
                  {
                    Add4.map((similarity, key) => <option key={key} value={key}>{similarity}
                    </option>)
                  }
                </select>
              </div>
              <div className="advSearch-module">
                <label><h2>Include Descendant Terms</h2></label>
                <select className="form-select2" aria-label="" onChange={e => { handleDescendantTermChanges(e) }}>
                  {
                    Add3.map((descendantTerm, key) => <option key={key} value={key}>{descendantTerm}
                    </option>)
                  }
                </select>
              </div>




            </div>


          </div>}



        </form>

        {showAdvSearch && <button className='returnBasic' onClick={handleBasicSearch}>BACK TO BASIC SEARCH</button>}



      </nav>

      <div>

        <ReactModal
          isOpen={isOpenModal1}
          onRequestClose={handleCloseModal1}
          shouldCloseOnOverlayClick={true}
        >
          <button onClick={handleCloseModal1}><img className="closeLogo" src="./cancel.png" alt='cancelIcon'></img></button>

          <p>Help for alphanumerical and numerical queries.</p>

        </ReactModal>
        <ReactModal
          isOpen={isOpenModal2}
          onRequestClose={handleCloseModal2}
          shouldCloseOnOverlayClick={true}
        >
          <button onClick={handleCloseModal2}><img className="closeLogo" src="./cancel.png" alt='cancelIcon'></img></button>

          <p>Help for queries.</p>

        </ReactModal>
      </div>


      <hr></hr>
      <div className="results">
        {results === null && !showFilteringTerms && <ResultsDatasets />}
        {results === 'Individuals' && <Individuals2 query={query} resultSets={resultSet} ID={ID} operator={operator} value={value} descendantTerm={descendantTerm} similarity={similarity} />}
        {results === null && showFilteringTerms && <FilteringTermsIndividuals filteringTerms={filteringTerms} collection={collection} setPlaceholder={setPlaceholder} placeholder={placeholder} />}
        {cohorts && results === 'Cohorts' &&

          <div>
            <Cohorts />
          </div>}
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
        <Route path='/individuals' element={<Individuals2 />} />
        <Route path='/genomicVariations' element={<GenomicVariations />} />
        <Route path='/biosamples' element={<Biosamples />} />
        <Route path='/runs' element={<Runs />} />
        <Route path='/analyses' element={<Analyses />} />
        <Route path='/cohorts' element={<Cohorts />} />
        <Route path='/datasets' element={<Datasets />} />
        <Route path='/members' element={<ResultsDatasets />} />
        <Route path='/history' element={<History />} />
        <Route path='/sign-up' element={<SignUpForm />} />
        <Route path="/sign-in" element={<SignInForm />} />
        <Route path="*" element={<ErrorPage />} />
      </Routes>
    </div>
  );
}



export default App;