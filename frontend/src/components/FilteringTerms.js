import { useState, useEffect } from "react"

function FilteringTerms(props) {

    const [error, setError] = useState(0)


    useEffect(() => {
        if (props.filteringTerms === false) {
            setError(true)
        } else {
            setError(false)
        }
     
     }, [error])

  


    return (
        <div>
            {error && <h3>No filtering terms available. Please select a collection and retry</h3>}
            {props.filteringTerms.data != undefined && props.filteringTerms.data.response.resultSets[0].results.map((term) => {
                return (<>

                    {Object.keys(term).map((key) => {
                        return (
                            <div>
                                <h2>{key}</h2>
                                <h2>{term[key]}</h2>
                            </div>

                        )

                    })}
                </>
                )
            })
            }
        </div>
    )
}

export default FilteringTerms