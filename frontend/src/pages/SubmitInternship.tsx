import Form from "../components/Features/InternshipCreateForm";
import { useEffect } from 'react';

// This component that renders the internship creation form
function Intranet() {

  useEffect(() => {
    // Add a class to the body or a wrapper when this page is rendered
    document.body.classList.add('page-submit');
    
    // Cleanup: Remove the class when the component unmounts
    return () => {
      document.body.classList.remove('page-submit');
    };
  }, []);
  
  return (
      <Form />
  );
}

export default Intranet;