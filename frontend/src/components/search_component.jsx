import React, { useState } from "react";
import "./search_component.css"; // Asegúrate de tener un archivo CSS para estilos

const SearchComponent = () => {
  const [query, setQuery] = useState(""); // Para la consulta
  const [model, setModel] = useState("tfidf"); // Para el modelo
  const [results, setResults] = useState([]); // Para los resultados

  // Función para manejar la entrada de texto de la consulta
  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  // Función para manejar el cambio de modelo
  const handleModelChange = (e) => {
    setModel(e.target.value);
  };

  // Función para manejar la búsqueda
  const handleSearch = async () => {
    if (!query) return; // Evitar búsqueda vacía

    try {
      const response = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query, model }),
      });

      const data = await response.json();
      if (response.ok) {
        setResults(data.results); // Actualizar el estado con los resultados
      } else {
        console.error("Error en la búsqueda:", data.error);
        setResults([]); // Si hay un error, asegurarse de que no se muestren resultados
      }
    } catch (error) {
      console.error("Error al obtener resultados:", error);
      setResults([]); // Si hay un error en la petición, no mostrar resultados
    }
  };

  return (
    <div className="search-container">
      <h1>Buscador de Documentos</h1>

      {/* Barra de consulta */}
      <input
        type="text"
        value={query}
        onChange={handleQueryChange}
        placeholder="Escribe tu consulta"
        className="input"
      />

      {/* Menú desplegable para seleccionar el modelo */}
      <select value={model} onChange={handleModelChange} className="select">
        <option value="tfidf">TF-IDF</option>
        <option value="bm25">BM25</option>
      </select>

      {/* Botón de búsqueda */}
      <button onClick={handleSearch} className="search-button">
        Buscar
      </button>

      {/* Mostrar los resultados */}
      <div className="results">
        <h2>Resultados</h2>
        {results.length > 0 ? (
          <ul className="results-list">
            { results.map((result, index) => (
              <li key={index}>
                <strong>{result.id}</strong>: {result.text}
              </li>
            ))}
          </ul>
        ) : (
          <p>No se encontraron resultados.</p>
        )}
      </div>
    </div>
  );
};

export default SearchComponent;