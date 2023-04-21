import { useState, useEffect } from "react"
import './FilteringTerms.css';

function FilteringTerms(props) {

    console.log(props)

    const [error, setError] = useState(false)

    const [checked, setChecked] = useState(false)

    const [counter, setCounter] = useState(0)


    const [state, setstate] = useState({
        query: '',
        list: props.filteringTerms !== false ? props.filteringTerms.data.response.filteringTerms : "error"
    })




    useEffect(() => {
        if (state.list === "error") {
            setError(true)
        } else {
            setError(false)
        }

        setstate({
            query: '',
            list: props.filteringTerms !== false ? props.filteringTerms.data.response.filteringTerms : "error"
        })


    }, [props.filteringTerms])


    const handleChange = (e) => {

        const results = props.filteringTerms.data.response.filteringTerms.filter(post => {
            console.log(post)
            if (e.target.value === "") {
                return props.filteringTerms.data.response.filteringTerms
            } else {
                if (post.id != undefined && post.label != undefined)  {
                    if (post.id.toLowerCase().includes(e.target.value.toLowerCase()) || post.label.toLowerCase().includes(e.target.value.toLowerCase())) {
                        return post
                    }
                } else {
                    if (post.id.toLowerCase().includes(e.target.value.toLowerCase())) {
                        return post
                    }
                }
            }

        })
        setstate({
            query: e.target.value,
            list: results
        })
      
    


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
                            <th className="search-box sorting" tabIndex="0" aria-controls="DataTables_Table_0" rowSpan="1" colSpan="2" aria-sort="ascending" aria-label=": activate to sort column descending"><form><input className="searchTermInput1" type="search" value={state.query} onChange={handleChange} placeholder="Search term" /></form></th>

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
                            <th className="th2">term</th>
                            <th className="th1">label</th>
                            <th className="th1">type</th>
                            <th className="th1">scope</th>
                        </tr>
                    </thead>
                    {props.filteringTerms.data !== undefined && state.list !== "error" && state.list.map((term, index) => {
                        return (<>


                            <tbody>

                                {index % 2 === 0 && <tr className="terms1">
                                    <td className="th2"><input className="select-checkbox" onClick={handleCheck} type="checkbox" id="includeTerm" name="term" value={term.id} />
                                        {term.id}</td>
                                    {term.label !== '' ? <td className="th1">{term.label}</td> : <td className="th1">-</td>}
                                    <td className="th1">{term.type}</td>
                                    <td className="th1">{term.scope}</td>
                                </tr>}
                                {index % 2 ==! 0 && <tr className="terms2">
                                    <td className="th2"><input className="select-checkbox"  onClick={handleCheck} type="checkbox" id="includeTerm" name="term" value={term.id} />
                                        {term.id}</td>
                                    {term.label !== '' ? <td className="th1">{term.label}</td> : <td className="th1">-</td>}
                                    <td className="th1">{term.type}</td>
                                    <td className="th1">{term.scope}</td>
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