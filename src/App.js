import { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, ScatterChart, Scatter, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';


function App() {
  const [data, setData] = useState({});
  const [trainExistingDf, setTrainExistingDf] = useState([]);
  const [testExistingDf, setTestExistingDf] = useState([]);
  const [trainPlot, setTrainPlot] = useState([]);
  const [testPlot, setTestPlot] = useState([]);
  const [xTrain, setXTrain] = useState([]);
  const [yTrain, setYTrain] = useState([]);
  const [xTest, setXTest] = useState([]);
  const [yTest, setYTest] = useState([]);
  const [predTest, setPredTest] = useState([]);
  const [number, setNumber] = useState('');
  const [numberTovar, setNumberTovar] = useState('');
  const [sortByT1, setSortByT1] = useState('date');
  const [sortOrderT1, setSortOrderT1] = useState('asc'); 
  const [sortByT2, setSortByT2] = useState('date');
  const [sortOrderT2, setSortOrderT2] = useState('asc'); 

  const [trainData, setTrainData] = useState([]);
  const [testData, setTestData] = useState([]);


  const fetchData = (value) => {
    axios.post(`http://127.0.0.1:5000/get_data_and_plot`, { number: parseInt(value) })
      .then(res => {
        setData(res.data);
        setTrainExistingDf(JSON.parse(res.data.train_existing_df))
        setTestExistingDf(JSON.parse(res.data.test_existing_df))
        setTrainPlot(JSON.parse(res.data.train_existing_df))
        setTestPlot(JSON.parse(res.data.test_existing_df))
        setXTrain(JSON.parse(res.data.x_train))
        setYTrain(JSON.parse(res.data.y_train))
        setXTest(JSON.parse(res.data.x_test))
        setYTest(JSON.parse(res.data.y_test))
        setPredTest(res.data.pred_test)
        setNumberTovar(value);
      })
      .catch(error => {
        console.error('Помилка отримання даних товару:', error);
      });
  }

  const fetchDataTaintTest = () => {
  axios.get('http://127.0.0.1:5000/get_train_and_test_data')
    .then(res => {
      setTrainData(JSON.parse(res.data.TRAIN_EXISTING_DF_COMBINED));
      setTestData(JSON.parse(res.data.TEST_EXISTING_DF_COMBINED));
    })
    .catch(error => {
      console.error('Помилка отримання даних:', error);
    });
};




  const handleMultiply = () => {
    if (parseInt(number) < 1 || parseInt(number) > 111) {
      alert('Будь ласка, введіть значення від 1 до 111');
    } else {
      fetchData(number);
      setNumber('');
    }
  }

  const handleKeyPress = (e) => {
  if (e.key === 'Enter') {
      handleMultiply();
    }
  }

  const handleSortChangeT1 = (e) => {
    setSortByT1(e.target.value); // Функція обробника для зміни параметру сортування
  };

  const handleOrderChangeT1 = (e) => {
    setSortOrderT1(e.target.value); // Функція обробника для зміни порядку сортування
  };

  trainExistingDf.sort((a, b) => {
    const order = sortOrderT1 === 'asc' ? 1 : -1;
    if (a[sortByT1] < b[sortByT1]) {
      return -1 * order;
    }
    if (a[sortByT1] > b[sortByT1]) {
      return 1 * order;
    }
    return 0;
  });


  const handleSortChangeT2 = (e) => {
    setSortByT2(e.target.value); // Функція обробника для зміни параметру сортування
  };

  const handleOrderChangeT2 = (e) => {
    setSortOrderT2(e.target.value); // Функція обробника для зміни порядку сортування
  };

  testExistingDf.sort((a, b) => {
    const order = sortOrderT2 === 'asc' ? 1 : -1;
    if (a[sortByT2] < b[sortByT2]) {
      return -1 * order;
    }
    if (a[sortByT2] > b[sortByT2]) {
      return 1 * order;
    }
    return 0;
  });


  
const plot1 = trainPlot.map(item => {
  const { date, units } = item;
  const formattedDate = `${new Date(date).getFullYear()}-${String(new Date(date).getMonth() + 1).padStart(2, '0')}-${String(new Date(date).getDate()).padStart(2, '0')}`;
  return { date: formattedDate, units };});
const plot2 = testPlot.map(item => {
  const { date, units } = item;
  const formattedDate = `${new Date(date).getFullYear()}-${String(new Date(date).getMonth() + 1).padStart(2, '0')}-${String(new Date(date).getDate()).padStart(2, '0')}`;
  return { date: formattedDate, units }; 
});
  

const plot3 = [
    // Додаємо дані для Train y(x)
    ...xTrain.map((value, index) => ({ x: value.dayofyear, y: yTrain[index], type: 'Train y(x)' })),
    // Додаємо дані для Test y(x)
    ...xTest.map((value, index) => ({ x: value.dayofyear, y: yTest[index], type: 'Test y(x)' })),
    // Додаємо дані для Test predict
    ...xTest.map((value, index) => ({ x: value.dayofyear, y: predTest[index], type: 'Test predict' })),
  ];


 

   // Викликати fetchData при завантаженні компоненту зі значенням 1
  useEffect(() => {
    setNumberTovar(1)
    fetchData(1);
    fetchDataTaintTest();
  }, []);

  
 

  return (
    <div className='conteiner'>
      {(trainExistingDf.length > 0 && testExistingDf.length>0) ? ( 
        <div>
          <h1>Walmart Recruiting II: Sales in Stormy Weather</h1>
 
{/* ============================================================== */}

          {/* ============================================================== */}
          <div className='plot'>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={trainData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="item_nbr" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="units" name="Train data" stroke="#8884d8" />
              </LineChart>
            </ResponsiveContainer>    
          </div>
          <div className='plot'>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={testData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="item_nbr" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="units" name="Test data" stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
          </div>
          
{/* ============================================================== */}

          <h2>Аналіз конкретного товару</h2>
          <div className='form'> 
            <label htmlFor="inputField">Введіть номер товару:</label>
            <input className='input'
              id="inputField"
              type="number"
              value={number}
              onChange={e => setNumber(e.target.value)}
              min={1}
              max={111}
              onKeyPress={handleKeyPress} />
            </div>
            <button className='button' onClick={handleMultiply}>Відправити</button>
            <p> Номер товару: <span className='span'>{numberTovar}</span></p>
          

{/* ============================================================== */}
 
          <div className='table'>
            <h2>Тренувальні дані {numberTovar} товару</h2>
            <div className='tableSort'>
            <label htmlFor="sortSelectT1">Сортувати за:</label>
            <select className='tableSortselect' id="sortSelectT1" value={sortByT1} onChange={handleSortChangeT1}>
              <option value="date">Дата</option>
              <option value="store_nbr">№ магазину</option>
              <option value="item_nbr">№ товару</option>
              <option value="units">Кількість</option>
              <option value="station_nbr">№ станції</option>
              <option value="codesum">Код погоди</option>
              <option value="preciptotal">Опади</option>
              </select>
              <label htmlFor="orderSelect">Порядок сортування:</label>
              <select className='tableSortselect' id="orderSelect" value={sortOrderT1} onChange={handleOrderChangeT1}>
                <option value="asc">За зростанням</option>
                <option value="desc">За спаданням</option>
              </select>
              </div>
            <table>
              <thead>
                <tr>
                  <th>Дата</th>
                  <th>№ магазину</th>
                  <th>№ товару</th>
                  <th>Кількість</th>
                  <th>№ станції</th>
                  <th>Код погоди</th>
                  <th>Опади</th>
                </tr>
              </thead>
            </table>
            <div style={{ overflowY: 'scroll', height: '100%' }}>
              <table>
                  <tbody>
                  {trainExistingDf.map((row, index) => (
                      <tr key={index}>
                      <td>{`${new Date(row.date).getFullYear()} - ${String(new Date(row.date).getMonth() + 1).padStart(2, '0')} - ${String(new Date(row.date).getDate()).padStart(2, '0')}`}</td>
                        <td>{row.store_nbr}</td>
                        <td>{row.item_nbr}</td>
                        <td>{row.units}</td>
                        <td>{row.station_nbr}</td>
                        <td>{row.codesum}</td>
                        <td>{row.preciptotal}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
            </div>
          </div>


{/* ============================================================== */}


          <div className='table'>
            <h2>Тестові дані {numberTovar} товару</h2>
            <div className='tableSort'>
            <label htmlFor="sortSelectT1">Сортувати за:</label>
            <select className='tableSortselect' id="sortSelectT1" value={sortByT2} onChange={handleSortChangeT2}>
              <option value="date">Дата</option>
              <option value="store_nbr">№ магазину</option>
              <option value="item_nbr">№ товару</option>
              <option value="units">Кількість</option>
              <option value="station_nbr">№ станції</option>
              <option value="codesum">Код погоди</option>
              <option value="preciptotal">Опади</option>
              </select>
              <label htmlFor="orderSelect">Порядок сортування:</label>
              <select className='tableSortselect' id="orderSelect" value={sortOrderT1} onChange={handleOrderChangeT2}>
                <option value="asc">За зростанням</option>
                <option value="desc">За спаданням</option>
              </select>
              </div>
            <table>
              <thead>
                <tr>
                  <th>Дата</th>
                  <th>№ магазину</th>
                  <th>№ товару</th>
                  <th>Кількість</th>
                  <th>№ станції</th>
                  <th>Код погоди</th>
                  <th>Опади</th>
                </tr>
              </thead>
            </table>
            <div style={{ overflowY: 'scroll', height: '100%' }}>
              <table>
                  <tbody>
                    {testExistingDf.map((row, index) => (
                      <tr key={index}>
                        <td>{`${new Date(row.date).getFullYear()} - ${String(new Date(row.date).getMonth() + 1).padStart(2, '0')} - ${String(new Date(row.date).getDate()).padStart(2, '0')}`}</td>
                        <td>{row.store_nbr}</td>
                        <td>{row.item_nbr}</td>
                        <td>{row.units}</td>
                        <td>{row.station_nbr}</td>
                        <td>{row.codesum}</td>
                        <td>{row.preciptotal}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
            </div>
          </div>

{/* ============================================================== */}
          <div className='leftText'>
            <p>Загальна кількість проданого товару train: <span className='span'>{data.train_total_units}</span></p>
            <p>Загальна кількість проданого товару test: <span className='span'>{data.test_total_units}</span></p>
          </div>

{/* ============================================================== */}
          <div className='plot'>
          <ResponsiveContainer width="50%" height={400}>
        <LineChart data={plot1}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="units" name="Train data" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
      <ResponsiveContainer width="50%" height={400}>
        <LineChart data={plot2}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="units" name="Test data" stroke="#82ca9d" />
        </LineChart>
          </ResponsiveContainer>
          </div>

{/* ============================================================== */}
          <div className='leftText'>
            <p>Сума помилок на тренувальних даних: <span className='span'>{data.rmsle_train}</span></p>
            <p>Сума помилок на тестових даних: <span className='span'>{data.rmsle_test}</span></p>
          </div>
{/* ============================================================== */}
          <div className='plot'>
      <ScatterChart width={800} height={400}>
      <CartesianGrid />
      <XAxis type="number" dataKey="x" name="Day of Year" />
      <YAxis type="number" dataKey="y" name="Value" />
      <Tooltip cursor={{ strokeDasharray: '3 3' }} />
      <Legend />
      <Scatter name="Train y(x)" data={plot3.filter(entry => entry.type === 'Train y(x)')} fill="#8884d8" />
      <Scatter name="Test y(x)" data={plot3.filter(entry => entry.type === 'Test y(x)')} fill="#82ca9d" />
      <Scatter name="Test predict" data={plot3.filter(entry => entry.type === 'Test predict')} fill="red" />
    </ScatterChart>
</div>
        </div>
        ) : (
        <div><span class="loader"></span></div>
      )}
      



    </div>
  );
}

export default App;





