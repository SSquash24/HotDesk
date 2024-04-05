import { useState } from "react";
import { useMemo, useEffect } from "react";

export default function usePersistState(initial_value, id) {
    //set init value
    const _initial_value = useMemo(() => {
        const local_storage_value_str = localStorage.getItem('state:'+id);
        // if there is a value stored, use that
        if (local_storage_value_str) {
            return JSON.parse(local_storage_value_str);
        }

        // otherwise use initial_value
        return initial_value
    }, [])

    const [state, setState] = useState(_initial_value)

    // useEffect(() => {
    //     const state_str = JSON.stringify(state);
    //     localStorage.setItem('state' + id, state_str)
    // }, [state])

    function wrappedSetState(newState) {
        const state_str = JSON.stringify(newState);
        localStorage.setItem('state:' + id, state_str)
        setState(newState)
    }

    return [state, wrappedSetState]
    // return [state, setState]
}