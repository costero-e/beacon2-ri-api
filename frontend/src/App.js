
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
  const [showAlphanumValue, setAlphanumValue] = useState(false)
  const [resultSetType, setResultsetType] = useState(["Select", "HIT", "MISS", "NONE", "ALL"])
  const [resultSet, setResultset] = useState("HIT")

  const [limit, setLimit] = useState(10)
  const [skip, setSkip] = useState(0)


  const [ID, setId] = useState("")
  const [operator, setOperator] = useState("")
  const [value, setValue] = useState("")


  const [descendantTermType, setDescendantTermType ] = useState(["true", "false"])
  const [descendantTerm, setDescendantTerm] = useState("true")

  const [similarityType, setSimilarityType] = useState(["Select", "low", "medium", "high"])
  const [similarity, setSimilarity] = useState("Select")

  const Add = collectionType.map(Add => Add)

  const Add2 = resultSetType.map(Add2 => Add2)

  const Add3 = descendantTermType.map(Add3 => Add3)

  const Add4 = similarityType.map(Add4 => Add4)

  const handleAddrTypeChange = (e) => {

    setCollection(collectionType[e.target.value])
    setExampleQ([])

  }

  const handleClick = (e) => {
    setCollectionType(["Select", "Individuals", "Cohorts", "Datasets", "Biosamples", "Analyses", "Runs", "Variant"])
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

  const handleSkipChanges = (e) => {
    setSkip(e.target.value)
  }

  const handleLimitChanges = (e) => {
    setLimit(e.target.value)
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
    setValue(e.target.vlue)
  }

  const handleAlphanumSearch = (e) => {
    setAlphanumValue(true)
  }

  const handleBasicSearch = (e) => {
    setAdvSearch(false)
    setAlphanumValue(false)
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

    setCollectionType(["Select"])


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
      <nav className="navbar">
        <div className="container-fluid">
          <select className="form-select" aria-label="Default select example" onClick={handleClick} onChange={e => { handleAddrTypeChange(e) }}>
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

        <div className="additionalOptions">

          {!showAdvSearch && <button className="advSearch" onClick={handleAdvancedSearch}>
            Advanced search
          </button>}
          <div className="example">
            <button className="exampleQueries" onClick={handleExQueries}>Query Examples</button>
            <img className="bulbLogo" src="../light-bulb.png" alt='bulbIcon'></img>
            <div>
              {exampleQ[0] && exampleQ.map((result) => {

                return (<div id='exampleQueries'>

                  <button className="exampleQuery" onClick={() => { setPlaceholder(`${result}`); setQuery(`${result}`); setResults(null) }} >{result}</button>
                </div>)

              })}
            </div>

          </div>
          {!showAlphanumValue && <button className="advSearch" onClick={handleAlphanumSearch}>
            Alphanumerical Value Query
          </button>}


        </div>

        <form className='advSearchForm' onSubmit={onSubmit}>

          {showAdvSearch && <div>

            <hr></hr>
            <div className='advSearchModule'>
              <div>
                <label>SKIP</label>
                <input className="skipForm" type="number" autoComplete='on' placeholder={0} onChange={(e) => handleSkipChanges(e)} aria-label="Skip" />
              </div>
              <div>
                <label>LIMIT</label>
                <input className="limitForm" type="number" autoComplete='on' placeholder={10} onChange={(e) => handleLimitChanges(e)} aria-label="Limit" />
              </div>
              <div className='resultset'>
                <label>Include Resultset Responses</label>
                <select className="form-select2" aria-label="" onChange={e => { handleResultsetChanges(e) }}>
                  {
                    Add2.map((resultSet, key) => <option key={key} value={key}>{resultSet}
                    </option>)
                  }
                </select>
              </div>

            </div>
            <div className='advSearchModule2'>
              <div> 
              
                <label>Similarity</label>
                <select className="form-select2" aria-label="" onChange={e => { handleSimilarityChanges(e) }}>
                  {
                    Add4.map((similarity, key) => <option key={key} value={key}>{similarity}
                    </option>)
                  }
                </select>
              </div>
              <div>
                <label>Include Descendant Terms</label>
                <select className="form-select2" aria-label="" onChange={e => { handleDescendantTermChanges(e) }}>
                  {
                    Add3.map((descendantTerm, key) => <option key={key} value={key}>{descendantTerm}
                    </option>)
                  }
                </select>
               
              </div>

            </div>
          </div>}


          {showAlphanumValue && <div className='alphanumContainer'>
            <hr></hr>
            <div className='alphanumContainer2'>
              <label>ID</label>
              <input className="IdForm" type="text" autoComplete='on' placeholder={"write the ID"} onChange={(e) => handleIdChanges(e)} aria-label="ID" />
              <label>Operator</label>
              <input className="OperatorForm" type="text" autoComplete='on' placeholder={"="} onChange={(e) => handleOperatorChanges(e)} aria-label="Operator" />
              <label>Value</label>
              <input className="ValueForm" type="text" autoComplete='on' placeholder={"free text/ value"} onChange={(e) => handleValueChanges(e)} aria-label="Value" />
            </div>

          </div>}
          {(showAlphanumValue || showAdvSearch) && <button className="searchButton" type="submit"><img className="searchIcon" src="./magnifier.png" alt='searchIcon'></img></button>}
        </form>



      </nav>

      {(showAlphanumValue || showAdvSearch) && <button className='returnBasic' onClick={handleBasicSearch}>RETURN TO BASIC SEARCH</button>}

      <hr></hr>
      <div className="results">
        {results === null && <ResultsDatasets />}
        {results === 'Individuals' && <Individuals2 query={query} resultSets={resultSet} limit={limit} skip={skip} ID={ID} operator={operator} value={value} descendantTerm={descendantTerm} similarity={similarity}/>}
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

