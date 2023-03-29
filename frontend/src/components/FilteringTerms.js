import { useState, useEffect } from "react"

function FilteringTerms(props) {

    const [error, setError] = useState(false)


    if (props.filteringTerms === false) {
        setError("true")
    }


    console.log(props.filteringTerms)


    return (
        <div>
            {error && <h1>No collection selected</h1>}
            {error === false && props.filteringTerms.data.response.resultSets[0].results.map((term) => {
                return (<>ç

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