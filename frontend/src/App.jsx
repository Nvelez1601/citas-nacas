import Home from "./pages/Home.jsx";
import LilyParticles from "./components/LilyParticles.jsx";

function App() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      <LilyParticles />
      <div className="relative z-10">
        <Home />
      </div>
    </div>
  );
}

export default App;
