/**
 * Dashboard Page Component
 * 
 * This component displays expense statistics and summaries.
 * 
 * Why this file exists:
 * - Shows total expenses and counts
 * - Displays category-wise breakdown
 * - Shows monthly expense trends
 * - Provides quick overview of spending
 */

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const response = await api.get('/dashboard/summary')
      setDashboardData(response.data)
    } catch (err) {
      if (err.response?.status === 401) {
        // Token expired or invalid, redirect to login
        localStorage.removeItem('token')
        navigate('/login')
      } else {
        setError('Failed to load dashboard data')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  if (loading) {
    return <div style={styles.loading}>Loading...</div>
  }

  if (error) {
    return <div style={styles.error}>{error}</div>
  }

  if (!dashboardData) {
    return <div style={styles.error}>No data available</div>
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Expense Tracker Dashboard</h1>
        <button onClick={handleLogout} style={styles.logoutButton}>Logout</button>
      </div>

      <div style={styles.statsGrid}>
        <div style={styles.statCard}>
          <h3 style={styles.statTitle}>Total Expenses</h3>
          <p style={styles.statValue}>${dashboardData.total_expenses.toFixed(2)}</p>
          <p style={styles.statSubtitle}>{dashboardData.total_expense_count} expenses</p>
        </div>
        <div style={styles.statCard}>
          <h3 style={styles.statTitle}>This Month</h3>
          <p style={styles.statValue}>${dashboardData.current_month_total.toFixed(2)}</p>
          <p style={styles.statSubtitle}>{dashboardData.current_month_count} expenses</p>
        </div>
      </div>

      <div style={styles.section}>
        <h2 style={styles.sectionTitle}>Category Breakdown</h2>
        {dashboardData.category_summary.length === 0 ? (
          <p style={styles.noData}>No expense data available</p>
        ) : (
          <div style={styles.categoryList}>
            {dashboardData.category_summary.map((category, index) => (
              <div key={index} style={styles.categoryItem}>
                <div style={styles.categoryInfo}>
                  <span style={styles.categoryName}>{category.category}</span>
                  <span style={styles.categoryAmount}>${category.total_amount.toFixed(2)}</span>
                </div>
                <div style={styles.categoryDetails}>
                  <span style={styles.categoryCount}>{category.expense_count} expenses</span>
                  <span style={styles.categoryPercentage}>{category.percentage}%</span>
                </div>
                <div style={styles.progressBar}>
                  <div 
                    style={{
                      ...styles.progressFill,
                      width: `${category.percentage}%`
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div style={styles.section}>
        <h2 style={styles.sectionTitle}>Monthly Trends</h2>
        {dashboardData.monthly_expenses.length === 0 ? (
          <p style={styles.noData}>No monthly data available</p>
        ) : (
          <div style={styles.monthlyList}>
            {dashboardData.monthly_expenses.map((month, index) => (
              <div key={index} style={styles.monthlyItem}>
                <span style={styles.monthName}>{month.month}</span>
                <span style={styles.monthAmount}>${month.total_amount.toFixed(2)}</span>
                <span style={styles.monthCount}>{month.expense_count} expenses</span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div style={styles.navButtons}>
        <button onClick={() => navigate('/expenses')} style={styles.navButton}>
          Manage Expenses
        </button>
      </div>
    </div>
  )
}

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '30px'
  },
  title: {
    margin: 0,
    color: '#333'
  },
  logoutButton: {
    padding: '10px 20px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px'
  },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
    marginBottom: '30px'
  },
  statCard: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
  },
  statTitle: {
    margin: '0 0 10px 0',
    color: '#666',
    fontSize: '14px'
  },
  statValue: {
    margin: '0 0 5px 0',
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#333'
  },
  statSubtitle: {
    margin: 0,
    color: '#999',
    fontSize: '14px'
  },
  section: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    marginBottom: '20px'
  },
  sectionTitle: {
    margin: '0 0 20px 0',
    color: '#333'
  },
  categoryList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px'
  },
  categoryItem: {
    padding: '15px',
    backgroundColor: '#f8f9fa',
    borderRadius: '4px'
  },
  categoryInfo: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '5px'
  },
  categoryName: {
    fontWeight: 'bold',
    color: '#333'
  },
  categoryAmount: {
    fontWeight: 'bold',
    color: '#007bff'
  },
  categoryDetails: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '10px',
    fontSize: '14px',
    color: '#666'
  },
  categoryCount: {},
  categoryPercentage: {},
  progressBar: {
    height: '8px',
    backgroundColor: '#e9ecef',
    borderRadius: '4px',
    overflow: 'hidden'
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#007bff',
    transition: 'width 0.3s ease'
  },
  monthlyList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px'
  },
  monthlyItem: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '15px',
    backgroundColor: '#f8f9fa',
    borderRadius: '4px'
  },
  monthName: {
    fontWeight: 'bold',
    color: '#333'
  },
  monthAmount: {
    fontWeight: 'bold',
    color: '#007bff'
  },
  monthCount: {
    color: '#666',
    fontSize: '14px'
  },
  navButtons: {
    display: 'flex',
    gap: '10px',
    marginTop: '20px'
  },
  navButton: {
    padding: '12px 24px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px'
  },
  loading: {
    textAlign: 'center',
    padding: '50px',
    fontSize: '18px',
    color: '#666'
  },
  error: {
    textAlign: 'center',
    padding: '50px',
    fontSize: '18px',
    color: '#dc3545'
  },
  noData: {
    color: '#999',
    textAlign: 'center',
    padding: '20px'
  }
}

export default Dashboard
