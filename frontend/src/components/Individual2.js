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
<<<<<<< HEAD
<<<<<<< HEAD
=======
  const [operator, setOperator] = useState([])
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
  const [operator, setOperator] = useState([])
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
  const [timeOut, setTimeOut] = useState(false)

  const API_ENDPOINT = "http://localhost:5050/api/individuals/"

  let queryStringTerm = ''
  let queryArray = []
  let keyTerm = []
  let resultsAux = []
  let obj = {}
<<<<<<< HEAD
<<<<<<< HEAD

  useEffect(() => {
    const apiCall = async () => {

=======
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
  let res = ""

  useEffect(() => {
    const apiCall = async () => {
      console.log(props.query)
      console.log(props.resultSets)
      console.log(props.limit)
<<<<<<< HEAD
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900

      if (props.query != null) {

        queryStringTerm = props.query.split(',')
<<<<<<< HEAD
<<<<<<< HEAD

=======
        console.log(queryStringTerm)
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
        console.log(queryStringTerm)
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
        queryStringTerm.forEach((element, index) => {

          element = element.trim()

          if (element.includes('=')) {

            queryArray[index] = element.split('=')

<<<<<<< HEAD
<<<<<<< HEAD
            queryArray[queryArray.length] = '='

          } else if (element.includes('>')) {
            queryArray[index] = element.split('>')
            queryArray[queryArray.length] = '>'

          } else if (element.includes('<')) {
            queryArray[index] = element.split('<')
            queryArray[queryArray.length] = '<'
=======
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
            queryArray[index].push('=')

          } else if (element.includes('>')) {
            queryArray[index] = element.split('>')
            queryArray[index].push('>')

          } else if (element.includes('<')) {
            queryArray[index] = element.split('<')
            queryArray[index].push('<')
          } else {
            queryArray[index] = element
<<<<<<< HEAD
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
          }
        })

        console.log(queryArray)

<<<<<<< HEAD
<<<<<<< HEAD
=======


>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======


>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
      }

      try {
        if (props.query === null) {

          var jsonData1 = {

            "meta": {
              "apiVersion": "2.0"
            },
            "query": {
              "filters": [],
<<<<<<< HEAD
<<<<<<< HEAD
              "includeResultsetResponses": "HIT",
              "pagination": {
                "skip": 0,
                "limit": 100
=======
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
              "includeResultsetResponses": `${props.resultSets}`,
              "pagination": {
                "skip": `${props.skip}`,
                "limit": `${props.limit}`
<<<<<<< HEAD
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
              },
              "testMode": false,
              "requestedGranularity": "record",
            }
          }

<<<<<<< HEAD
<<<<<<< HEAD
          jsonData1 = JSON.stringify(jsonData1)

          const res = await axios.post("http://localhost:5050/api/individuals/", jsonData1)
=======
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900




          jsonData1 = JSON.stringify(jsonData1)
          console.log(jsonData1)

          const res = await axios.post("https://ega-archive.org/beacon-apis/cineca/individuals/", jsonData1)
<<<<<<< HEAD
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900


          setNumberResults(res.data.responseSummary.numTotalResults)
          setBoolean(res.data.responseSummary.exists)
<<<<<<< HEAD
<<<<<<< HEAD

=======
          setTimeOut(true)
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
          setTimeOut(true)
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
          res.data.response.resultSets[0].results.forEach((element, index) => {

            results.push(res.data.response.resultSets[0].results[index])


          })

        } else if (!(props.query.includes('=')) && !(props.query.includes('<')) && !(props.query.includes('>'))) {

<<<<<<< HEAD
<<<<<<< HEAD
          const res = await axios.get(`https://ega-archive.org/beacon-apis/cineca/individuals/?filters=${props.query}`)
          console.log("loading")
=======
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
          if (props.resultSets === "HIT" && props.limit === 10) {

            res = await axios.get(`https://ega-archive.org/beacon-apis/cineca/individuals/?filters=${props.query}`)

          } else {
            var jsonData2 = {

              "meta": {
                "apiVersion": "2.0"
              },
              "query": {
                "filters": [],
                "includeResultsetResponses": `${props.resultSets}`,
                "pagination": {
                  "skip": `${props.skip}`,
                  "limit": `${props.limit}`
                },
                "testMode": false,
                "requestedGranularity": "record",
              }
            }
  
            
            jsonData2 = JSON.stringify(jsonData2)
            console.log(jsonData2)

            res = await axios.post("https://ega-archive.org/beacon-apis/cineca/individuals/", jsonData2)

          }


<<<<<<< HEAD
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
          setTimeOut(true)


          if (res.data.response.resultSets[0].results[0] === undefined) {
            setError("No results. Please check the query and retry")
<<<<<<< HEAD
<<<<<<< HEAD
            setNumberResults(res.data.responseSummary.numTotalResults)
            setBoolean(res.data.responseSummary.exists)
=======
            setNumberResults(0)
            setBoolean(false)
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
            setNumberResults(0)
            setBoolean(false)
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900

          }
          else {
            res.data.response.resultSets[0].results.forEach((element, index) => {

              results.push(res.data.response.resultSets[0].results[index])


            })
<<<<<<< HEAD
<<<<<<< HEAD
            console.log(res.data.responseSummary.numTotalResults)
=======

>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======

>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
            setNumberResults(res.data.responseSummary.numTotalResults)
            setBoolean(res.data.responseSummary.exists)
          }




        } else {

<<<<<<< HEAD
<<<<<<< HEAD
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
=======
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900

          let res = null

          for (let i = 0; i < queryArray.length; i++) {

            keyTerm = queryArray[i]
            console.log(keyTerm)
            console.log(typeof keyTerm)

            if (typeof keyTerm === "object") {

              label.push(keyTerm[0].trim())
              ident.push(keyTerm[1].trim())
              operator.push(keyTerm[2].trim())

            }

            if (typeof keyTerm === "string") {
              ident.push(keyTerm.trim())
            }


          }


          console.log(label)
          console.log(ident)
          console.log(operator)


          let arrayFilter = []

          operator.forEach((element, index) => {

            if (element === '>') {

              const filter = {
                "id": label[index],
                "operator": ">",
                "value": ident[index]
              }

              arrayFilter.push(filter)


            } else if (element === '<') {
              const filter = {
                "id": label[index],
                "operator": "<",
                "value": ident[index]
              }

              arrayFilter.push(filter)
            } else {
              ident.forEach((element, index) => {
                arrayFilter.push({ "id": ident[index] })
              })

            }
<<<<<<< HEAD
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
          })

          console.log(arrayFilter)

          if (arrayFilter.length > 1) {


            let stringIds = ident.join()
            console.log(stringIds)


            try {

<<<<<<< HEAD
<<<<<<< HEAD
              res = await axios.get(`https://ega-archive.org/beacon-apis/cineca/individuals/?filters=${stringIds}`)
=======
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
              if (props.resultSets === 'HIT') {
                res = await axios.get(`https://ega-archive.org/beacon-apis/cineca/individuals/?filters=${stringIds}`)
              }

<<<<<<< HEAD
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900

              setTimeOut(true)
            } catch (error) {
              setError("No results. Please check the query and retry")
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
<<<<<<< HEAD
<<<<<<< HEAD
                  "limit": 100
=======
                  "limit": `${props.limit}`
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
                  "limit": `${props.limit}`
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
                },
                "testMode": false,
                "requestedGranularity": "record",
              }
            }

            jsonData = JSON.stringify(jsonData)
            console.log(jsonData)

            res = await axios.post("https://ega-archive.org/beacon-apis/cineca/individuals/", jsonData)
            setTimeOut(true)
          }


          setNumberResults(res.data.responseSummary.numTotalResults)
          setBoolean(res.data.responseSummary.exists)

          res.data.response.resultSets[0].results.forEach((element, index) => {

            results.push(res.data.response.resultSets[0].results[index])


          })

          let entries = Object.entries(results[0])
          console.log(entries)
<<<<<<< HEAD
<<<<<<< HEAD

        }

      } catch (error) {
        console.log(error)
        setError(error.message)
=======
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
        }


      } catch (error) {

        setError("No results found. Please check the query and retry")
<<<<<<< HEAD
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
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
    <div> {timeOut &&
      <div className='selectGranularity'>
        <button className='typeResults' onClick={handleTypeResults1}> Boolean</button>
        <button className='typeResults' onClick={handleTypeResults2}>Count</button>
        <button className='typeResults' onClick={handleTypeResults3}>Full</button>
      </div>}

      <div className='resultsContainer'>
        {show1 && boolean && <p className='p1'>YES</p>}
        {show1 && !boolean && <p className='p1'>N0</p>}

        {show2 && numberResults !== 1 && <p className='p1'>{numberResults} &nbsp; Results</p>}
        {show2 && numberResults === 1 && <p className='p1'>{numberResults} &nbsp; Result</p>}

        {show3 && <div className="results">

          {!error && results[0] && results.map((result) => {


            return (
              <div className="resultsIndividuals">

<<<<<<< HEAD
<<<<<<< HEAD

                {result.id && <h2>ID</h2>}
                {result.id && <h3>{result.id}</h3>}
                {result.diseases && <h2>Disease</h2>}

                {result.diseases && result.diseases.map((value) => {
                  return (
                    <div>
                      <h3>{value.diseaseCode.id}</h3>
                      <h3>{value.diseaseCode.label}</h3>
                    </div>)
                })}




                {result.ethnicity && <h2>Ethnicity</h2>}
                {result.ethnicity && <h3>{result.ethnicity.id}</h3>}
                {result.ethnicity && <h3>{result.ethnicity.label}</h3>}
                {result.geographicOrigin && <h2>Geographic Origin</h2>}
                {result.geographicOrigin && <h3>{result.geographicOrigin.id}</h3>}
                {result.geographicOrigin && <h3>{result.geographicOrigin.label}</h3>}
                {result.sex && <h2>Sex</h2>}
                {result.sex.id && <h3>{result.sex.id}</h3>}
                {result.sex.label && <h3>{result.sex.label}</h3>}

=======
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900
                <div>
                  {result.id && <h2>ID</h2>}
                  {result.id && <h3>{result.id}</h3>}
                  {result.diseases && <h2>Disease</h2>}

                  {result.diseases && result.diseases.map((value) => {
                    return (
                      <div className='diseasesContainer'>
                        <h3>{value.diseaseCode.id}</h3>
                        <h3>{value.diseaseCode.label}</h3>
                      </div>)
                  })}

                </div>

                <div>
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
                <div className='measuresContainer'>
                  {result.measures && <h2>Measures</h2>}
                  {result.measures.map((value) => {
                    return (
                      <div className='measures'>
                        <div>
                          <h4>assayCode ID:</h4>
                          <h3>{value.assayCode.id}</h3>
                        </div>
                        <div>
                          <h4>assayCode label:</h4>
                          <h3>{value.assayCode.label}</h3>
                        </div>
                        
                        <div>
                          <h4>Measurament value quantity ID and label:</h4>
                          <h3>{value.measurementValue.quantity.unit.id}</h3>
                          <h3>{value.measurementValue.quantity.unit.label}</h3>
                        </div>
                        <div>
                          <h4>Measurament value quantity value:</h4>
                          <h3>{value.measurementValue.quantity.value}</h3>
                        </div>
                      </div>)
                  })}
                </div>
<<<<<<< HEAD
>>>>>>> fd17b7ffa5f8b77461f9a808437dcc13a5a978b0
=======
>>>>>>> c0195f3f78eaf95362a89d2fbb04113a4d83d900

              </div>
            )

          })}

          {error && <h3>&nbsp; {error} </h3>}
        </div>
        }
      </div>
    </div >

  )
}

export default Individuals2