import { useState } from 'react';
import axios from 'axios';

const useCompareCharacters = () => {
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const compareCharacters = async (name1, name2) => {
        setLoading(true);
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/compare`, {
                params: { name1, name2 }
            });
            setResult(response.data);
            setError('');
        } catch (err) {
            setError('One or both characters not found');
            setResult(null);
            console.error('Error fetching comparison:', err);
        } finally {
            setLoading(false);
        }
    };

    return { result, error, loading, compareCharacters };
};

export default useCompareCharacters;
