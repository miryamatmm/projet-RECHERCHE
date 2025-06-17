import { useState, useEffect } from 'react';
import '../../App.css';
import Keyword from '../UI/Inputs/Keyword';
import PeriodInput from '../UI/Inputs/PeriodInput';
import UniversitySelector from './UniversitySelector';
import MultiSelect from '../UI/Inputs/MultiSelect';
import {internshipGateway} from "../../adapters"
import { buildHierarchy } from '../../utils';
import { SearchResults, SearchParams } from '../../types';

type InternshipListProps = {
  searchResults: SearchResults;
  setSearchResults: any;
  loading: boolean;
  setLoading: any;
  searchParams: any;
  setSearchParams: any;
};

// This component provides the search functionality for internships.
function SearchBar({searchResults, setSearchResults, loading, setLoading, setSearchParams} : InternshipListProps){
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [periodValue, setPeriodValue] = useState<[Date | null, Date | null]>([new Date(), new Date(new Date().setFullYear(new Date().getFullYear() + 1))]);
  const [keyword, setKeyword] = useState<string>('');
  const [university, setUniversity] = useState<string>("-1")
  const [keywords, setKeywords] = useState<string[]>([]);
  const [options, setOptions] = useState([]);

  // Search function triggered on clicking the search button
  const search = async () => {
    let params: SearchParams = {
      keywords: keywords,
      discipline_ids: selectedOptions.map((e) => e.id),
      start_date: periodValue[0]?.toISOString().split('T')[0],
      end_date: periodValue[1]?.toISOString().split('T')[0],
      university_id: university,
      page: searchResults.page,
      page_size: searchResults.total_pages
    };
    setLoading(true)
    setSearchResults(await internshipGateway.search(params))
    setLoading(false)
  }

  // Build hierarchy from fetched disciplines
  useEffect(() => {
    const fetchData = async () => {
      const disciplines = await internshipGateway.disciplines();
      const h = buildHierarchy(disciplines)
      setOptions(h);
    };

    fetchData();
  }, []);

  // Add the keyword to the list and reset the keyword input field
  const handleAdd = () => {
    if (keyword.trim() !== '') {
      setKeywords([...keywords, keyword.trim()]); 
      setKeyword(''); 
    }
  };

  // Delete keyword by index
  const handleDelete = (index: number) => {
    setKeywords(keywords.filter((_, i) => i !== index)); 
  };

  return (
    <div className='w-full mt-5'>
      <div className='flex flex-col sm:flex-row mx-auto justify-center items-center gap-2 sm:h-auto'>
        <div className='flex border-2 border-golden rounded btn w-[80%] sm:w-auto order-1 sm:order-none'>
          <input className='w-full border-none bg-transparent px-4 py-2 outline-none focus:outline-none' type='search' value={keyword} onChange={(e) => setKeyword(e.target.value)} placeholder='Keyword'/>
          <button id='addBtn' className='m-1 rounded bg-golden px-4 text-white outline-none focus:outline-none py-2 flex items-center' type='button' onClick={handleAdd}>
            Add
          </button>
        </div>

        <div className='order-2 sm:order-none'>
          <PeriodInput range={periodValue} setRange={setPeriodValue} />
        </div>
        <div className='order-3 sm:order-none'>
          <UniversitySelector onSelectuniv={(univ) => { setUniversity(univ); }} />
        </div>

        <div className='sm:w-[20%] w-[85%] max-w-md order-4 sm:order-none'>
          <MultiSelect options={options} setOptions={setOptions} setSelectedOptions={setSelectedOptions} selectedOptions={selectedOptions} />
        </div>

        <div className='order-5 sm:order-none'>
          <button className='rounded bg-golden px-4 text-white outline-none focus:outline-none py-2 h-full flex items-center' type='submit' onClick={search}>
            Search
          </button>
        </div>
      </div>

      <div className='flex mt-5 mx-auto w-[50%] gap-3'>
        {keywords.map((keyword, index) => (
          <Keyword key={index} keyword={keyword} onDelete={() => handleDelete(index)} />
        ))}
      </div>
    </div>

  );
}

export default SearchBar;
