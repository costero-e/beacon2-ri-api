import './Individuals.css';
import '../App.css';
import { useState, useEffect } from 'react';
import axios from "axios";


function Individuals2(props) {


  const [error, setError] = useState(false)
  const [response, setResponse] = useState(null)
  const [numberResults, setNumberResults] = useState(0)
  const [boolean, setBoolean] = useState(false)
  const [results, setResults] = useState([])
  const [show1, setShow1] = useState(false)
  const [show2, setShow2] = useState(false)
  const [show3, setShow3] = useState(false)
  const [label, setLabel] = useState([])
  const [ident, setId] = useState([])

  const API_ENDPOINT = "http://localhost:5050/api/individuals/"

  let queryStringTerm = ''
  let queryArray = []
  let keyTerm = []
  let resultsAux = []
  let obj = {}

  useEffect(() => {
    const apiCall = async () => {


      if (props.query != null) {
        queryStringTerm = props.query.split(',')
      
        queryStringTerm.forEach((element, index) => {
       
          if (element.includes('=')) {
            queryArray[index] = element.split('=')
           
            queryArray[2] = '='

          } else if (element.includes('>')) {
            queryArray[index] = element.split('>')
            queryArray[2] = '>'

          } else if (element.includes('<')) {
            queryArray[index] = element.split('<')
            queryArray[2] = '<'
          }
        })

        console.log(queryArray)

      }

      try {
        if (props.query === null) {

          var jsonData1 = {

            "meta": {
              "apiVersion": "2.0"
            },
            "query": {
              "filters": [],
              "includeResultsetResponses": "HIT",
              "pagination": {
                "skip": 0,
                "limit": 100
              },
              "testMode": false,
              "requestedGranularity": "record",
            }
          }

          jsonData1 = JSON.stringify(jsonData1)

          const res = await axios.post("http://localhost:5050/api/individuals/", jsonData1)


          setNumberResults(res.data.responseSummary.numTotalResults)
          setBoolean(res.data.responseSummary.exists)

          res.data.response.resultSets[0].results.forEach((element, index) => {

            results.push(res.data.response.resultSets[0].results[index])


          })

        } else if (!(props.query.includes('=')) && !(props.query.includes('<')) && !(props.query.includes('>'))) {
          const res = await axios.post(API_ENDPOINT + props.query + '/')

          if (res.data.response.resultSets[0].results[0] === undefined) {
            setError("Individual not found")
            setNumberResults(res.data.responseSummary.numTotalResults)
            setBoolean(res.data.responseSummary.exists)

          }
          else {
            res.data.response.resultSets[0].results.forEach((element, index) => {

              results.push(res.data.response.resultSets[0].results[index])


            })
            setNumberResults(res.data.responseSummary.numTotalResults)
            setBoolean(res.data.responseSummary.exists)
          }

        } else {

          keyTerm[2] = queryArray[2]
          let res = null

          for (let i = 0; i < queryArray.length - 1; i++) {

            keyTerm = queryArray[i]

            label.push(keyTerm[0])

            ident.push(keyTerm[1])

            console.log(label)
            console.log(ident)


            if (keyTerm[2] === '<') {
              setError('Operator < does not match the term. Use = instead.')
            }
            if (keyTerm[2] === '>') {
              setError('Operator > does not match the term. Use = instead.')
            }

          }

          let arrayFilter = []
          label.forEach((element, index) => {
            arrayFilter.push({ "id": ident[index] })
          })

          console.log(arrayFilter)

          if (arrayFilter.length > 1) {
           
            let stringIds = ident.join()

            try {
           
              res = await axios.get(`https://localhost:5050/api/individuals/${stringIds}`)
              console.log(res)
            } catch (error) {
              setError(error)
            }

          }

          else {
            var jsonData = {

              "meta": {
                "apiVersion": "2.0"
              },
              "query": {
                "filters": arrayFilter,
                "includeResultsetResponses": "HIT",
                "pagination": {
                  "skip": 5,
                  "limit": 100
                },
                "testMode": false,
                "requestedGranularity": "record",
              }
            }

            jsonData = JSON.stringify(jsonData)
            console.log(jsonData)

            res = await axios.post("http://localhost:5050/api/individuals/", jsonData)

          }


          setNumberResults(res.data.responseSummary.numTotalResults)
          setBoolean(res.data.responseSummary.exists)

          res.data.response.resultSets[0].results.forEach((element, index) => {

            results.push(res.data.response.resultSets[0].results[index])


          })

          let entries = Object.entries(results[0])
          console.log(entries)

        }

      } catch (error) {
        console.log(error)
        setError(error.message)
      }
    };
    apiCall();
  }, [])


  const handleTypeResults1 = () => {
    setShow1(true)
    setShow2(false)
    setShow3(false)
  }

  const handleTypeResults2 = () => {
    setShow2(true)
    setShow1(false)
    setShow3(false)

  }

  const handleTypeResults3 = () => {
    setShow3(true)
    setShow1(false)
    setShow2(false)
  }

  return (
    <div>
      <div className='selectGranularity'>
        <button className='typeResults' onClick={handleTypeResults1}> Boolean</button>
        <button className='typeResults' onClick={handleTypeResults2}>Count</button>
        <button className='typeResults' onClick={handleTypeResults3}>Full</button>
      </div>

      <div className='resultsContainer'>
        {show1 && boolean && <p className='p1'>YES</p>}
        {show1 && !boolean && <p className='p1'>N0</p>}

        {show2 && numberResults !== 1 && <p className='p1'>{numberResults} &nbsp; Results</p>}
        {show2 && numberResults === 1 && <p className='p1'>{numberResults} &nbsp; Result</p>}

        {show3 && <div className="results">

          {!error && results[0] && results.map((result) => {


            return (
              <div className="resultsIndividuals">


                {result.id && <h2>ID</h2>}
                {result.id && <h3>{result.id}</h3>}
                {result.diseases && <h2>Disease</h2>}
                {result.diseases && <h3>{result.diseases[0].diseaseCode.id}</h3>}
                {result.diseases && <h3>{result.diseases[0].diseaseCode.label}</h3>}

                {result.ethnicity && <h2>Ethnicity</h2>}
                {result.ethnicity && <h3>{result.ethnicity.id}</h3>}
                {result.ethnicity && <h3>{result.ethnicity.label}</h3>}
                {result.geographicOrigin && <h2>Geographic Origin</h2>}
                {result.geographicOrigin && <h3>{result.geographicOrigin.id}</h3>}
                {result.geographicOrigin && <h3>{result.geographicOrigin.label}</h3>}
                {result.sex && <h2>Sex</h2>}
                {result.sex.id && <h3>{result.sex.id}</h3>}
                {result.sex.label && <h3>{result.sex.label}</h3>}


              </div>
            )

          })}

          {error && <h3>&nbsp; {error} </h3>}
        </div>
        }
      </div>
    </div>

  )
}

export default Individuals2