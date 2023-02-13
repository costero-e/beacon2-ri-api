import './Individuals.css';
import '../App.css';
import { useState, useEffect } from 'react';
import axios from "axios";

function Individuals(props) {

    const [error, setError] = useState(null)
    const [response, setResponse] = useState(null)
    const [numberResults, setNumberResults] = useState(0)
    const [results, setResults] = useState([])
    const [show1, setShow1] = useState(false)
    const [show2, setShow2] = useState(false)
    const [show3, setShow3] = useState(false)

    const API_ENDPOINT = "http://localhost:5050/api/individuals/"

    let queryStringTerm = ''
    let queryArray = []
    let keyTerm = []
    let resultsAux = []
    let obj = {}

    useEffect(() => {
        const apiCall = async () => {
            console.log(props.query)

            if (props.query != null) {
                queryStringTerm = props.query.split(',')
                console.log(queryStringTerm)

                queryStringTerm.forEach((element, index) => {
                    element = element.split(' ').join('')

                    if (element.includes('=')) {
                        queryArray[index] = element.split('=')

                    } else if (element.includes('>')) {
                        queryArray[index] = element.split('>')

                    } else if (element.includes('<')) {
                        queryArray[index] = element.split('<')

                    }


                })


            }


            try {
                if (props.query === null) {
                    const res = await axios.get(API_ENDPOINT);
                    console.log(res)
                    setNumberResults(res.data.response.resultSets[0].results.length)

                    res.data.response.resultSets[0].results.forEach((element, index) => {

                        results.push(res.data.response.resultSets[0].results[index])


                    })

                } else if (!(props.query.includes('=')) && !(props.query.includes('<')) && !(props.query.includes('>'))) {
                    const res = await axios.post(API_ENDPOINT + props.query)

                    if (res.data.response.resultSets[0].results[0] === undefined) {
                        setError("Individual not found")
                    }
                    else {
                        results.push(res.data.response.resultSets[0].results[0])
                    }

                } else {
                    const res = await axios.post(API_ENDPOINT)

                    for (let i = 0; i < queryArray.length; i++) {

                        keyTerm = queryArray[i]

                        res.data.response.resultSets[0].results.forEach((element, index) => {


                            if (keyTerm[0] === 'ethnicity') {

                                if (keyTerm[3] === '=') {
                                    if (element[keyTerm[0].label] === keyTerm[2] || element[keyTerm[0].id] === keyTerm[2]) {
                                        resultsAux.push(element)
                                    }
                                }
                                if (keyTerm[3] === '<') {
                                    setError('Operator < does not match the ethnicity term. Use = instead.')
                                }
                                if (keyTerm[3] === '>') {
                                    setError('Operator > does not match the ethnicity term. Use = instead.')
                                }

                            }

                            if (keyTerm[0] === 'geographicOrigin') {

                                if (keyTerm[3] === '=') {
                                    if (element[keyTerm[0].label] === keyTerm[2] || element[keyTerm[0].id] === keyTerm[2]) {
                                        resultsAux.push(element)
                                    }
                                }
                                if (keyTerm[3] === '<') {
                                    setError('Operator < does not match the ethnicity term. Use = instead.')
                                }
                                if (keyTerm[3] === '>') {
                                    setError('Operator > does not match the ethnicity term. Use = instead.')
                                }

                            }

                            if (keyTerm[0] === 'sex') {
                                if (keyTerm[2] = '=') {
                                    obj = element[keyTerm[0]]

                                    if (obj.label === keyTerm[1] || obj.id === keyTerm[1]) {
                                        resultsAux.push(element)
                                    }
                                }
                                if (keyTerm[3] === '<') {
                                    setError('Operator < does not match the ethnicity term. Use = instead.')
                                }
                                if (keyTerm[3] === '>') {
                                    setError('Operator > does not match the ethnicity term. Use = instead.')
                                }

                            }

                            if (keyTerm[0] === 'phenotypicFeatures') {

                                if (keyTerm[3] === '=') {
                                    if (element[keyTerm[0]][0].featureType.label === keyTerm[2] || element[keyTerm[0]][0].featureType.id === keyTerm[2]) {
                                        resultsAux.push(element)
                                    }
                                }
                                if (keyTerm[3] === '<') {
                                    setError('Operator < does not match the ethnicity term. Use = instead.')
                                }
                                if (keyTerm[3] === '>') {
                                    setError('Operator > does not match the ethnicity term. Use = instead.')
                                }

                            }

                            if (keyTerm[0] === 'diseases') {

                                if (keyTerm[3] === '=') {
                                    if (element[keyTerm[0]][0].diseaseCode.label === keyTerm[2] || element[keyTerm[0]][0].diseaseCode.id === keyTerm[2]) {
                                        resultsAux.push(element)
                                    }
                                }
                                if (keyTerm[3] === '<') {
                                    setError('Operator < does not match the ethnicity term. Use = instead.')
                                }
                                if (keyTerm[3] === '>') {
                                    setError('Operator > does not match the ethnicity term. Use = instead.')
                                }

                            }


                        })

                        res.data.response.resultSets[0].results = resultsAux

                    }



                    setResults(resultsAux)

                    setNumberResults(resultsAux.length)


                    console.log(results)


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
            <button className='typeResults' onClick={handleTypeResults1}> Boolean</button>
            <button className='typeResults' onClick={handleTypeResults2}>Count</button>
            <button className='typeResults' onClick={handleTypeResults3}>Full</button>

            {show1 && numberResults !== 0 && <p className='p1'>YES</p>}
            {show1 && numberResults === 0 && <p className='p1'>N0</p>}

            {!error && show2 && numberResults !== 1 && <p className='p1'>{numberResults} &nbsp; Results</p>}
            {!error && show2 && numberResults === 1 && <p className='p1'>{numberResults} &nbsp; Result</p>}


            {show3 && <div className="results">
                {!error && results[0] && results.map((result) => {
                    return (
                        <div className="resultsIndividuals">
                            <div>
                                <h3>{result.id}</h3>
                                <h2>Disease</h2>
                                <h3>{result.diseases[0].diseaseCode.id}</h3>
                                <h3>{result.diseases[0].diseaseCode.label}</h3>
                                <h2>Ethnicity</h2>
                                <h3>{result.ethnicity.id}</h3>
                                <h3>{result.ethnicity.label}</h3>
                                <h2>Geographic Origin</h2>
                                <h3>{result.geographicOrigin.id}</h3>
                                <h3>{result.geographicOrigin.label}</h3>
                                <h2>Sex</h2>
                                <h3>{result.sex.id}</h3>
                                <h3>{result.sex.label}</h3>
                            </div>
                        </div>
                    )
                })}

                {error && <h3>&nbsp; {error} </h3>}
            </div>
            }
        </div>

    )
}

export default Individuals