import { useState, useEffect } from "react"
import './FilteringTerms.css';

function FilteringTerms(props) {

    console.log(props)
    const [error, setError] = useState(false)

    const [checked, setChecked] = useState(false)

    const [counter, setCounter] = useState(0)


    const [state, setstate] = useState({
        query: '',
        list: props.FilteringTerms !== undefined ? props.filteringTerms.data.response.filteringTerms : "error"
    })




    useEffect(() => {
        if (state.list === "error"){
            setError(true)
        }

        setstate({
            query: '',
            list: props.FilteringTerms !== undefined ? props.filteringTerms.data.response.filteringTerms : "error"
        })

      
    }, [props.filteringTerms])


    const handleChange = (e) => {

   
        const results = props.filteringTerms.data.response.resultSets[0].results.filter(post => {
            if (e.target.value === "") {
                return props.filteringTerms.data.response.resultSets[0].results
            } else {
                if (post.id.toLowerCase().includes(e.target.value.toLowerCase()) || post.label.toLowerCase().includes(e.target.value.toLowerCase())) {
                    return post
                }

            }

        })
        setstate({
            query: e.target.value,
            list: results
        })




    }

    const onChange = (e) => {

    }

    const handleCheck = (e) => {

        if (props.placeholder.includes(e.target.value)) {

            let stringQuery = props.placeholder

            if (stringQuery.includes(',')) {
                stringQuery = stringQuery.replace(`,${e.target.value}`, '')
                stringQuery = stringQuery.replace(`${e.target.value},`, '')
            } else {
                stringQuery = stringQuery.replace(e.target.value, '')
            }



            if (stringQuery === '' || stringQuery === ',') {
                props.setPlaceholder('key=value, key><=value, or filtering term comma-separated')
            } else {
                props.setPlaceholder(stringQuery)
            }


        } else {
            if ((e.target.value != props.placeholder) && (props.placeholder != 'key=value, key><=value, or filtering term comma-separated')) {
                let stringQuery = `${props.placeholder},` + e.target.value
                stringQuery = stringQuery.replace('key=value, key><=value, or filtering term comma-separated', '')
                props.setPlaceholder(stringQuery)
            } else {
                let stringQuery = e.target.value
                stringQuery = stringQuery.replace('key=value, key><=value, or filtering term comma-separated', '')
                props.setPlaceholder(stringQuery)
            }


        }



    }

    console.log(state.list)



    return (
        <div>
            {error && <h3>No filtering terms available. Please select a collection and retry</h3>}

            {!error && <div className="tableWrapper">

                <table className="table">
                    <thead>
                        <tr className="search-tr">
                            <th className="search-box sorting" tabIndex="0" aria-controls="DataTables_Table_0" rowSpan="1" colSpan="2" aria-sort="ascending" aria-label=": activate to sort column descending"><form><input className="searchTermInput" type="search" value={state.query} onChange={handleChange} placeholder="Search term" /></form></th>

                        </tr>
                        <tr className="search-tr">
                            <th className="search-box sorting" tabIndex="0" aria-controls="DataTables_Table_0" rowSpan="1" colSpan="2" aria-sort="ascending" aria-label=": activate to sort column descending"><form><input className="searchTermInput" type="search" value={state.query} onChange={handleChange} placeholder="Search term" /></form></th>

                        </tr>
                        <tr className="search-tr">
                            <th className="search-box sorting" tabIndex="0" aria-controls="DataTables_Table_0" rowSpan="1" colSpan="2" aria-sort="ascending" aria-label=": activate to sort column descending"><form><input className="searchTermInput" type="search" value={state.query} onChange={handleChange} placeholder="Search term" /></form></th>

                        </tr>
                        <tr className="search-tr">
                            <th className="search-box sorting" tabIndex="0" aria-controls="DataTables_Table_0" rowSpan="1" colSpan="2" aria-sort="ascending" aria-label=": activate to sort column descending"><form><input className="searchTermInput" type="search" value={state.query} onChange={handleChange} placeholder="Search term" /></form></th>

                        </tr>
                    </thead>
                    <thead>
                        <tr>
                            <th className="th1">filtering term</th>
                            <th className="th2">label</th>
                            <th className="th3">target entity</th>
                            <th className="th4">target schema term</th>
                        </tr>
                    </thead>
                    {props.filteringTerms.data !== undefined && state.list!== "error" && state.list.map((term) => {
                        return (<>


                            <tbody>

                                <tr className="terms1">
                                    <input className="select-checkbox" onChange={onChange} onClick={handleCheck} type="checkbox" id="includeTerm" name="term" value={term.id} />
                                    <td className="th1">{term.id}</td>
                                    {term.label !== '' ? <td className="th2">{term.label}</td> : <td className="th2">-</td>}
                                    <td className="th3">{term.collection}</td>
                                    <td className="th4">{term.type}</td>
                                </tr>
                                {term.label !== '' && <tr className="terms2">
                                    <input className="select-checkbox" type="checkbox" defaultChecked={checked} onClick={handleCheck} id="includeTerm2" name="term" value={term.label} />
                                    <td className="th1">{term.label}</td>
                                    <td className="th2">-</td>
                                    <td className="th3">{term.collection}</td>
                                    <td className="th4">{term.type}</td>
                                </tr>}

                            </tbody>






                        </>
                        )
                    })

                    }
                </table>
            </div>}
        </div>
    )
}

export default FilteringTerms