import "./App.css";
import Main from "./pages/Main";
import SubmitInternship from "./pages/SubmitInternship";
import MyInernships from "./pages/MyInternships";

import Login from "./pages/Login";
import Logout from "./pages/Logout"
import {internshipGateway} from "./adapters"

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { useAuth } from "./providers/Auth";

function App() {

  const menuHeight = 55;
  const { user } = useAuth();

  return (
    <>

      <div style={{top: "0px",  textAlign: "center", width: "100%", borderBottom: "solid 5px rgb(178 143 79 / var(--tw-bg-opacity, 1))"}}>
        {user !== null &&
          <span>
            <i>Hello {user.firstname} {user.lastname} from {user.university.name} !</i> <br/>
          </span>
        }
        <a href="/">Find an internships</a>
        &nbsp;|&nbsp;
        {user !== null &&
          <>
            <a href="/my_internships">My internships</a>
            &nbsp;|&nbsp;
            <a href="/submit">Submit a new internship</a>
          </>
        }
        {user === null &&
          <a href="/login">Login to submit a new internship</a>
        }
        {user !== null &&
          <span>
            &nbsp;|&nbsp;<a href="/logout">Logout</a>
          </span>
        }
      </div>
      <div>
        <Router>
          <Routes>
            <Route path="/" element={<Main />} />
            <Route path="/my_internships" element={<MyInernships />} />
            <Route path="/submit" element={<SubmitInternship />} />
            <Route path="/login" element={<Login />} />
            <Route path="/logout" element={<Logout/>}/>
          </Routes>
        </Router>
      </div>
    </>
  );
}

export default App;
