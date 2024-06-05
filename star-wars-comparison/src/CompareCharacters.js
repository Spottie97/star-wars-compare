import React, { useState, useMemo } from 'react';
import useCharacters from './hooks/useCharacters';
import useCompareCharacters from './hooks/useCompareCharacters';
import './App.css';

const attributeTitles = {
    name: 'Name',
    height: 'Height (cm)',
    mass: 'Mass (kg)',
    hair_color: 'Hair Color',
    skin_color: 'Skin Color',
    eye_color: 'Eye Color',
    birth_year: 'Birth Year',
    gender: 'Gender'
};

const CompareCharacters = () => {
    const [name1, setName1] = useState('');
    const [name2, setName2] = useState('');
    const [selectedName1, setSelectedName1] = useState('');
    const [selectedName2, setSelectedName2] = useState('');
    const { characters, loading: loadingCharacters, error: errorCharacters } = useCharacters();
    const { result, error, loading, compareCharacters } = useCompareCharacters();

    const handleCompare = () => {
        compareCharacters(name1, name2);
        setSelectedName1(name1);
        setSelectedName2(name2);
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    };

    const handleScrollToTop = () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const characterOptions = useMemo(() => characters.map(character => (
        <option key={character.name} value={character.name}>
            {character.name}
        </option>
    )), [characters]);

    return (
        <div className="app-container">
            <div className="video-background">
                <video autoPlay loop muted>
                    <source src="/star-wars-warp.mp4" type="video/mp4" />
                </video>
            </div>
            <div className="form-container">
                <h1>Compare Star Wars Characters</h1>
                {loadingCharacters ? (
                    <p className="star-wars-yellow">Loading Characters...</p>
                ) : errorCharacters ? (
                    <p>{errorCharacters}</p>
                ) : (
                    <div>
                        <select value={name1} onChange={(e) => setName1(e.target.value)}>
                            <option value="">Select First Character</option>
                            {characterOptions}
                        </select>
                        <select value={name2} onChange={(e) => setName2(e.target.value)}>
                            <option value="">Select Second Character</option>
                            {characterOptions}
                        </select>
                        <button onClick={handleCompare} disabled={!name1 || !name2}>Compare</button>
                    </div>
                )}
                {error && <p>{error}</p>}
            </div>
            {loading ? (
                <p className="star-wars-yellow">Loading Results...</p>
            ) : result && (
                <div className="result-container">
                    <div className="character-row">
                        <div className="character-column">
                            <h2>{selectedName1}</h2>
                            <img src={result.images.character1} alt={selectedName1} className="character-image" />
                            {Object.keys(result.comparison).map(attr => (
                                <div key={attr} className="character-attribute">
                                    <strong>{attributeTitles[attr] || attr}: </strong>{result.comparison[attr].character1}
                                    {result.comparison[attr].winner === 'character1' && <span> (Winner)</span>}
                                </div>
                            ))}
                        </div>
                        <div className="character-column">
                            <h2>{selectedName2}</h2>
                            <img src={result.images.character2} alt={selectedName2} className="character-image" />
                            {Object.keys(result.comparison).map(attr => (
                                <div key={attr} className="character-attribute">
                                    <strong>{attributeTitles[attr] || attr}: </strong>{result.comparison[attr].character2}
                                    {result.comparison[attr].winner === 'character2' && <span> (Winner)</span>}
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="result-summary star-wars-yellow">
                        {result.overall_winner === 'character1' && <h3>{selectedName1} is the overall winner!</h3>}
                        {result.overall_winner === 'character2' && <h3>{selectedName2} is the overall winner!</h3>}
                        {result.overall_winner === 'tie' && <h3>It's a tie!</h3>}
                    </div>
                    <button onClick={handleScrollToTop}>Back to Top</button>
                </div>
            )}
        </div>
    );
};

export default CompareCharacters;
