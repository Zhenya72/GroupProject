import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';


function App() {
  const [data, setData] = useState({});
  const [trainExistingDf, setTrainExistingDf] = useState([]);
  const [testExistingDf, setTestExistingDf] = useState([]);



  const fetchData = (value) => {
    axios.post(`http://127.0.0.1:5000/get_data_and_plot`, { number: parseInt(value) })
      .then(res => {
        setData(res.data);
        setTrainExistingDf(JSON.parse(res.data.train_existing_df))
        setTestExistingDf(JSON.parse(res.data.test_existing_df))
      })
      .catch(error => {
        console.error('Помилка отримання даних:', error);
      });
  }





 

   // Викликати fetchData при завантаженні компоненту зі значенням 1
  useEffect(() => {
    fetchData();
  }, []);

  
 

  return (
    <div className='conteiner'>
      {(trainExistingDf.length > 0 && testExistingDf.length>0) ? ( 
        <div>
          <h1>Walmart Recruiting II: Sales in Stormy Weather</h1>
 
{/* ============================================================== */}

          {/* ============================================================== */}

          
{/* ============================================================== */}

          <h2>Аналіз конкретного товару</h2>
          
          

{/* ============================================================== */}
 



{/* ============================================================== */}



{/* ============================================================== */}
          <div className='leftText'>
            <p>Загальна кількість проданого товару train: <span className='span'>{data.train_total_units}</span></p>
            <p>Загальна кількість проданого товару test: <span className='span'>{data.test_total_units}</span></p>
          </div>

{/* ============================================================== */}


{/* ============================================================== */}
          <div className='leftText'>
            <p>Сума помилок на тренувальних даних: <span className='span'>{data.rmsle_train}</span></p>
            <p>Сума помилок на тестових даних: <span className='span'>{data.rmsle_test}</span></p>
          </div>
{/* ============================================================== */}

        </div>
        ) : (
        <div><span class="loader"></span></div>
      )}
      



    </div>
  );
}

export default App;





