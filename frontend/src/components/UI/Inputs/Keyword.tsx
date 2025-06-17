// This component displays a single keyword.
function Keyword({ keyword, onDelete }: { keyword: string; onDelete: () => void }) {

  const keywordWidth = keyword.length + 150; 
  return (
    <div className='flex justify-between rounded border-2 border-golden px-2 items-center' style={{ width: `${keywordWidth}px` }}>
      <p>{keyword}</p>
      <button className='px-1 py-1 outline-none focus:outline-none' style={{borderColor: 'transparent'}} onClick={onDelete}>&times;</button>
    </div>
  );
}
  
  export default Keyword;
  