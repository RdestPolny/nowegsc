import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, Globe, Link, MousePointer, Eye, Calendar } from 'lucide-react';

const GSCDashboard = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [sites, setSites] = useState([]);
  const [selectedSite, setSelectedSite] = useState('');
  const [dateRange, setDateRange] = useState({ start: '2025-07-01', end: '2025-09-30' });
  const [selectedPeriod, setSelectedPeriod] = useState('custom');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [aggregation, setAggregation] = useState('month'); // 'day' or 'month'

  // Mock data dla demonstracji - rozszerzony do 16 miesięcy
  const generateMockData = () => {
    const dailyData = [];
    const startDate = new Date('2024-06-01');
    const endDate = new Date('2025-09-30');
    
    for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 7)) {
      const baseClicks = 400 + Math.random() * 200;
      const trend = (d - startDate) / (endDate - startDate) * 600;
      
      dailyData.push({
        date: d.toISOString().split('T')[0],
        clicks: Math.round(baseClicks + trend + Math.random() * 100),
        impressions: Math.round((baseClicks + trend) * 25 + Math.random() * 3000),
        ctr: 3.5 + Math.random() * 1.5,
        position: 9 - (d - startDate) / (endDate - startDate) * 4
      });
    }
    
    return dailyData;
  };

  const mockData = {
    timeSeriesData: generateMockData(),
    countryData: [
      { country: 'Polska', clicks: 8500, impressions: 185000, ctr: 4.59 },
      { country: 'USA', clicks: 1200, impressions: 32000, ctr: 3.75 },
      { country: 'Niemcy', clicks: 950, impressions: 28000, ctr: 3.39 },
      { country: 'UK', clicks: 720, impressions: 21000, ctr: 3.43 },
      { country: 'Francja', clicks: 580, impressions: 18500, ctr: 3.14 }
    ],
    topPages: [
      { page: '/blog/seo-tips-2025', clicks: 2100, impressions: 45000, ctr: 4.67, position: 4.2 },
      { page: '/produkty/kategoria-a', clicks: 1850, impressions: 42000, ctr: 4.40, position: 5.1 },
      { page: '/', clicks: 1600, impressions: 38000, ctr: 4.21, position: 3.8 },
      { page: '/blog/marketing-content', clicks: 1320, impressions: 35000, ctr: 3.77, position: 6.3 },
      { page: '/uslugi', clicks: 1100, impressions: 28000, ctr: 3.93, position: 5.8 },
      { page: '/blog/google-analytics', clicks: 980, impressions: 25000, ctr: 3.92, position: 7.1 },
      { page: '/kontakt', clicks: 850, impressions: 22000, ctr: 3.86, position: 8.2 },
      { page: '/o-nas', clicks: 720, impressions: 19000, ctr: 3.79, position: 6.9 }
    ],
    topQueries: [
      { query: 'optymalizacja seo', clicks: 1250, impressions: 28000, ctr: 4.46, position: 4.5 },
      { query: 'marketing internetowy', clicks: 1120, impressions: 26500, ctr: 4.23, position: 5.2 },
      { query: 'pozycjonowanie stron', clicks: 980, impressions: 24000, ctr: 4.08, position: 6.1 },
      { query: 'content marketing', clicks: 850, impressions: 21000, ctr: 4.05, position: 5.8 },
      { query: 'analityka google', clicks: 720, impressions: 19000, ctr: 3.79, position: 6.5 },
      { query: 'social media marketing', clicks: 650, impressions: 17500, ctr: 3.71, position: 7.2 },
      { query: 'strategia seo', clicks: 580, impressions: 15800, ctr: 3.67, position: 7.8 },
      { query: 'reklama google ads', clicks: 520, impressions: 14200, ctr: 3.66, position: 8.1 }
    ],
    deviceData: [
      { device: 'Mobile', clicks: 5800, impressions: 135000 },
      { device: 'Desktop', clicks: 4200, impressions: 98000 },
      { device: 'Tablet', clicks: 1000, impressions: 25000 }
    ]
  };

  const handleAuth = () => {
    setLoading(true);
    // Symulacja autoryzacji OAuth
    setTimeout(() => {
      setIsAuthenticated(true);
      setSites(['https://example.com', 'https://blog.example.com']);
      setLoading(false);
    }, 1500);
  };

  const setPeriod = (period) => {
    const today = new Date('2025-09-30');
    let startDate;
    
    switch(period) {
      case '1month':
        startDate = new Date(today);
        startDate.setMonth(startDate.getMonth() - 1);
        setAggregation('day');
        break;
      case '3months':
        startDate = new Date(today);
        startDate.setMonth(startDate.getMonth() - 3);
        setAggregation('month');
        break;
      case '12months':
        startDate = new Date(today);
        startDate.setMonth(startDate.getMonth() - 12);
        setAggregation('month');
        break;
      case '16months':
        startDate = new Date(today);
        startDate.setMonth(startDate.getMonth() - 16);
        setAggregation('month');
        break;
      default:
        return;
    }
    
    setDateRange({
      start: startDate.toISOString().split('T')[0],
      end: today.toISOString().split('T')[0]
    });
    setSelectedPeriod(period);
  };

  const aggregateDataByMonth = (data) => {
    const monthlyData = {};
    
    data.forEach(item => {
      const monthKey = item.date.substring(0, 7); // YYYY-MM
      
      if (!monthlyData[monthKey]) {
        monthlyData[monthKey] = {
          date: monthKey,
          clicks: 0,
          impressions: 0,
          positions: [],
          ctrs: []
        };
      }
      
      monthlyData[monthKey].clicks += item.clicks;
      monthlyData[monthKey].impressions += item.impressions;
      monthlyData[monthKey].positions.push(item.position);
      monthlyData[monthKey].ctrs.push(item.ctr);
    });
    
    return Object.values(monthlyData).map(month => ({
      date: month.date,
      clicks: month.clicks,
      impressions: month.impressions,
      ctr: month.ctrs.reduce((a, b) => a + b, 0) / month.ctrs.length,
      position: month.positions.reduce((a, b) => a + b, 0) / month.positions.length
    })).sort((a, b) => a.date.localeCompare(b.date));
  };

  const getFilteredData = () => {
    if (!data) return null;
    
    const filtered = data.timeSeriesData.filter(item => 
      item.date >= dateRange.start && item.date <= dateRange.end
    );
    
    return aggregation === 'month' ? aggregateDataByMonth(filtered) : filtered;
  };

  const handleSiteSelect = (site) => {
    setSelectedSite(site);
    setLoading(true);
    // Symulacja pobierania danych
    setTimeout(() => {
      setData(mockData);
      setLoading(false);
    }, 1000);
  };

  const StatCard = ({ icon: Icon, title, value, change, color }) => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm">{title}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
          {change && (
            <p className={`text-sm mt-1 ${change > 0 ? 'text-green-600' : 'text-red-600'}`}>
              {change > 0 ? '+' : ''}{change}% vs poprzedni okres
            </p>
          )}
        </div>
        <div className={`${color} p-3 rounded-lg`}>
          <Icon className="text-white" size={24} />
        </div>
      </div>
    </div>
  );

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center">
          <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <TrendingUp className="text-blue-600" size={32} />
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Google Search Console</h1>
          <p className="text-gray-600 mb-6">Połącz się z GSC, aby zobaczyć swoje dane analityczne</p>
          <button
            onClick={handleAuth}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Łączenie...' : 'Połącz z Google'}
          </button>
          <p className="text-xs text-gray-500 mt-4">
            Ta aplikacja używa OAuth 2.0 do bezpiecznego połączenia z GSC
          </p>
        </div>
      </div>
    );
  }

  if (!selectedSite) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-800 mb-6">Wybierz witrynę</h1>
          <div className="grid gap-4">
            {sites.map((site) => (
              <div
                key={site}
                onClick={() => handleSiteSelect(site)}
                className="bg-white rounded-lg shadow hover:shadow-lg transition p-6 cursor-pointer border-2 border-transparent hover:border-blue-500"
              >
                <div className="flex items-center">
                  <Globe className="text-blue-600 mr-4" size={32} />
                  <div>
                    <h3 className="text-xl font-semibold text-gray-800">{site}</h3>
                    <p className="text-gray-500">Kliknij, aby zobaczyć dane</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (loading || !data) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Ładowanie danych...</p>
        </div>
      </div>
    );
  }

  const totalClicks = data.timeSeriesData.reduce((sum, d) => sum + d.clicks, 0);
  const totalImpressions = data.timeSeriesData.reduce((sum, d) => sum + d.impressions, 0);
  const avgCTR = (totalClicks / totalImpressions * 100).toFixed(2);
  const avgPosition = (data.timeSeriesData.reduce((sum, d) => sum + d.position, 0) / data.timeSeriesData.length).toFixed(1);

  const filteredData = getFilteredData();
  const periodClicks = filteredData.reduce((sum, d) => sum + d.clicks, 0);
  const periodImpressions = filteredData.reduce((sum, d) => sum + d.impressions, 0);
  const periodCTR = (periodClicks / periodImpressions * 100).toFixed(2);
  const periodPosition = (filteredData.reduce((sum, d) => sum + d.position, 0) / filteredData.length).toFixed(1);

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Dashboard GSC</h1>
              <p className="text-gray-600 mt-1">{selectedSite}</p>
            </div>
          </div>
          
          {/* Period Selection Buttons */}
          <div className="flex flex-wrap gap-2 mb-4">
            <button
              onClick={() => setPeriod('1month')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                selectedPeriod === '1month'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 border hover:bg-gray-50'
              }`}
            >
              Ostatni miesiąc
            </button>
            <button
              onClick={() => setPeriod('3months')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                selectedPeriod === '3months'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 border hover:bg-gray-50'
              }`}
            >
              Kwartał (3 msc)
            </button>
            <button
              onClick={() => setPeriod('12months')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                selectedPeriod === '12months'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 border hover:bg-gray-50'
              }`}
            >
              Ostatnie 12 msc
            </button>
            <button
              onClick={() => setPeriod('16months')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                selectedPeriod === '16months'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 border hover:bg-gray-50'
              }`}
            >
              Ostatnie 16 msc
            </button>
          </div>
          
          {/* Custom Date Range */}
          <div className="flex flex-wrap gap-2 items-center">
            <span className="text-sm text-gray-600 font-medium">Własny zakres:</span>
            <input
              type="date"
              value={dateRange.start}
              onChange={(e) => {
                setDateRange({...dateRange, start: e.target.value});
                setSelectedPeriod('custom');
              }}
              className="border rounded px-3 py-2 text-sm"
            />
            <input
              type="date"
              value={dateRange.end}
              onChange={(e) => {
                setDateRange({...dateRange, end: e.target.value});
                setSelectedPeriod('custom');
              }}
              className="border rounded px-3 py-2 text-sm"
            />
            <select
              value={aggregation}
              onChange={(e) => setAggregation(e.target.value)}
              className="border rounded px-3 py-2 text-sm"
            >
              <option value="day">Dziennie</option>
              <option value="month">Miesięcznie</option>
            </select>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon={MousePointer}
            title="Kliknięcia w okresie"
            value={periodClicks.toLocaleString()}
            change={12.5}
            color="bg-blue-500"
          />
          <StatCard
            icon={Eye}
            title="Wyświetlenia w okresie"
            value={periodImpressions.toLocaleString()}
            change={8.3}
            color="bg-green-500"
          />
          <StatCard
            icon={TrendingUp}
            title="Średnie CTR"
            value={`${periodCTR}%`}
            change={5.2}
            color="bg-yellow-500"
          />
          <StatCard
            icon={Calendar}
            title="Średnia pozycja"
            value={periodPosition}
            change={-8.5}
            color="bg-purple-500"
          />
        </div>

        {/* Time Series Chart */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4">
            Ruch w czasie ({aggregation === 'month' ? 'miesięcznie' : 'dziennie'})
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={filteredData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="clicks" stroke="#3b82f6" strokeWidth={2} name="Kliknięcia" />
              <Line yAxisId="right" type="monotone" dataKey="impressions" stroke="#10b981" strokeWidth={2} name="Wyświetlenia" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* CTR and Position Chart */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4">
            CTR i Pozycja w czasie ({aggregation === 'month' ? 'miesięcznie' : 'dziennie'})
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={filteredData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" reversed />
              <Tooltip />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="ctr" stroke="#f59e0b" strokeWidth={2} name="CTR (%)" />
              <Line yAxisId="right" type="monotone" dataKey="position" stroke="#ef4444" strokeWidth={2} name="Pozycja" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Country and Device Distribution */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Ruch według krajów</h2>
            <div className="space-y-3">
              {data.countryData.map((country, idx) => (
                <div key={country.country}>
                  <div className="flex justify-between mb-1">
                    <span className="font-medium">{country.country}</span>
                    <span className="text-gray-600">{country.clicks.toLocaleString()} kliknięć</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${(country.clicks / data.countryData[0].clicks) * 100}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Ruch według urządzeń</h2>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={data.deviceData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({device, percent}) => `${device} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="clicks"
                >
                  {data.deviceData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Pages Table */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Najpopularniejsze strony</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Strona</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Kliknięcia</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Wyświetlenia</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">CTR</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Pozycja</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {data.topPages.map((page, idx) => (
                  <tr key={idx} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-800">{page.page}</td>
                    <td className="px-4 py-3 text-sm text-right">{page.clicks.toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm text-right">{page.impressions.toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm text-right">{page.ctr.toFixed(2)}%</td>
                    <td className="px-4 py-3 text-sm text-right">{page.position.toFixed(1)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Top Queries Table */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Najpopularniejsze zapytania</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Zapytanie</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Kliknięcia</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Wyświetlenia</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">CTR</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-gray-700">Pozycja</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {data.topQueries.map((query, idx) => (
                  <tr key={idx} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-800">{query.query}</td>
                    <td className="px-4 py-3 text-sm text-right">{query.clicks.toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm text-right">{query.impressions.toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm text-right">{query.ctr.toFixed(2)}%</td>
                    <td className="px-4 py-3 text-sm text-right">{query.position.toFixed(1)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GSCDashboard;
