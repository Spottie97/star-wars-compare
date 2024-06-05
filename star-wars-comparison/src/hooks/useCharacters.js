import { useState, useEffect } from 'react';
import axios from 'axios';

const useCharacters = () => {
    const [characters, setCharacters] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchCharacters = async () => {
            const cachedCharacters = localStorage.getItem('characters');
            if (cachedCharacters) {
                setCharacters(JSON.parse(cachedCharacters));
                setLoading(false);
            } else {
                try {
                    let allCharacters = [];
                    let nextPage = 'https://swapi.dev/api/people/';

                    while (nextPage) {
                        const response = await axios.get(nextPage);
                        allCharacters = [...allCharacters, ...response.data.results];
                        nextPage = response.data.next;
                    }

                    setCharacters(allCharacters);
                    localStorage.setItem('characters', JSON.stringify(allCharacters));
                } catch (error) {
                    setError('Error fetching character list');
                    console.error('Error fetching character list:', error);
                } finally {
                    setLoading(false);
                }
            }
        };

        fetchCharacters();
    }, []);

    return { characters, loading, error };
};

export default useCharacters;
