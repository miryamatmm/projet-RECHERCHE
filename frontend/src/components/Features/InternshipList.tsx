import { SearchResults } from "../../types";
import InternshipCard from "./InternshipCard";

type InternshipListProps = {
  searchResults: SearchResults;
  setSearchResults: any;
  loading: boolean;
  searchParams: any;
  setSearchParams: any;
};

// This component displays a list of internships with pagination
function InternshipList({searchResults, setSearchResults, loading, searchParams, setSearchParams} : InternshipListProps){

    // Filter out the deleted internship from the search results
    const handleDelete = (id: number) => { 
      searchResults.data = searchResults.data.filter((internship) => internship.id !== id)
      setSearchResults(searchResults)
    };

    // Update the page number in searchParams and trigger a search refresh
    const handlePageChange = (newPage: number) => {
      searchParams.page = newPage;
      setSearchParams(searchParams);
    };
   
    // Display loading message while fetching internships
    if (loading) {
      return <p>Loading internships...</p>;
    }

    // Function to render pagination buttons with the correct range of pages
    const renderPageButtons = () => {
      const pages = [];
      let startPage = Math.max(searchResults.page - 2, 1);
      let endPage = Math.min(searchResults.page + 2, searchResults.total_pages);
  
      if (startPage > 1) pages.push(1);
      if (startPage > 2) pages.push("...");
  
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }
  
      if (endPage < searchResults.total_pages - 1) pages.push("...");
      if (endPage < searchResults.total_pages) pages.push(searchResults.total_pages);
  
      return ( 
        <>
          <i>Showing {Math.min(searchResults.page_size, searchResults.total)} offers from a total of {searchResults.total} offers found</i> <br/>
          <button
            onClick={() => handlePageChange(searchResults.page - 1)}
            disabled={searchResults.page <= 1}
            className="cursor-pointer hover:underline"
          >
            Previous
          </button>
            {pages.map((page, index) => (

                <button
                  key={index}
                  onClick={() => handlePageChange(Number(page))}
                  disabled={page === searchResults.page}
                  style={{
                    margin: "0 4px",
                    backgroundColor: page === searchResults.page ? "#d3d3d3": "transparent",
                    cursor: "pointer"
                  }}
                  className="hover:underline"
                >
                  {page}
                </button>

          ))}
          <button
          onClick={() => handlePageChange(searchResults.page + 1)}
          disabled={searchResults.page >= searchResults.total_pages}
          className="cursor-pointer hover:underline"
          >
          Next
          </button>
        </>
      );
    };

  return (
    <>
    <br/>
      <div className="flex flex-wrap w-[90%] mx-auto">
        {searchResults.data.map((internship) => (
          <InternshipCard key={internship.id} internship={internship} onDelete={handleDelete} isMainPage={true}/>
        ))}
      </div>
      <center className="mt-5">{renderPageButtons()}</center>

    </>
  );
}


export default InternshipList;