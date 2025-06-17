import { useEffect, useState } from "react";
import InternshipList from "../components/Features/InternshipList";
import SearchBar from "../components/Features/InternshipSearchBar";
import { SearchParams, SearchResults, emptySearchPparams } from "../types";
import {internshipGateway} from "../adapters"

// This component is responsible for the page displaying internship search functionality and the results list.
function Main() {
  const [searchParams, setSearchParams] = useState<SearchParams>(emptySearchPparams);

  const [searchResults, setSearchResults] = useState({data: [], total: 0, page: 1, page_size: 10, total_pages: 1} as SearchResults)
  const [loading, setLoading] = useState(false);
  
  // useEffect runs to perform the initial search when the component is first rendered
  useEffect(() => {
    (async() => {
      setSearchResults(await internshipGateway.search(searchParams))
    })()
  }, [])

  // Function to update search parameters and fetch new results when the parameters change
  const listSetSearchParams = async (e) => {
    setSearchParams(e)
    setSearchResults(await internshipGateway.search(e))
  }

  return (
    <>
      <SearchBar searchResults={searchResults} setSearchResults={setSearchResults} setLoading={setLoading} loading={loading} searchParams={searchParams} setSearchParams={setSearchParams}/>

      <InternshipList searchResults={searchResults} setSearchResults={setSearchResults} setSearchParams={listSetSearchParams} searchParams={searchParams} loading={loading}/>
    </>
  );
}
export default Main;