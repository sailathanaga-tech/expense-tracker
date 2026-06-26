/**
 * Expenses Page Component
 * 
 * This component handles expense management (Create, Read, Update, Delete).
 * 
 * Why this file exists:
 * - Displays list of expenses
 * - Allows adding new expenses
 * - Allows editing existing expenses
 * - Allows deleting expenses
 * - Filters by category
 */

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const CATEGORIES = ['Food', 'Travel', 'Shopping', 'Bills', 'Entertainment', 'Other']

function Expenses() {
  const [expenses, setExpenses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editingExpense, setEditingExpense] = useState(null)
  const [filterCategory, setFilterCategory] = useState('')
  const navigate = useNavigate()

  const [formData, setFormData] = useState({
    title: '',
    amount: '',
    category: 'Food',
    date: '',
    notes: ''
  })

  useEffect(() => {
    fetchExpenses()
  }, [filterCategory])

  const fetchExpenses = async () => {
    try {
      const params = filterCategory ? { category: filterCategory } : {}
      const response = await api.get('/expenses/', { params })
      setExpenses(response.data.expenses)
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem('token')
        navigate('/login')
      } else {
        setError('Failed to load expenses')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    try {
      const expenseData = {
        ...formData,
        amount: parseFloat(formData.amount),
        date: new Date(formData.date).toISOString()
      }

      if (editingExpense) {
        await api.put(`/expenses/${editingExpense.id}`, expenseData)
      } else {
        await api.post('/expenses/', expenseData)
      }

      resetForm()
      fetchExpenses()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save expense')
    }
  }

  const handleEdit = (expense) => {
    setEditingExpense(expense)
    setFormData({
      title: expense.title,
      amount: expense.amount,
      category: expense.category,
      date: new Date(expense.date).toISOString().split('T')[0],
      notes: expense.notes || ''
    })
    setShowForm(true)
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this expense?')) {
      return
    }

    try {
      await api.delete(`/expenses/${id}`)
      fetchExpenses()
    } catch (err) {
      setError('Failed to delete expense')
    }
  }

  const resetForm = () => {
    setFormData({
      title: '',
      amount: '',
      category: 'Food',
      date: '',
      notes: ''
    })
    setEditingExpense(null)
    setShowForm(false)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  if (loading) {
    return <div style={styles.loading}>Loading...</div>
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Manage Expenses</h1>
        <div style={styles.headerButtons}>
          <button onClick={() => navigate('/dashboard')} style={styles.backButton}>
            Back to Dashboard
          </button>
          <button onClick={handleLogout} style={styles.logoutButton}>Logout</button>
        </div>
      </div>

      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.controls}>
        <select
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value)}
          style={styles.filter}
        >
          <option value="">All Categories</option>
          {CATEGORIES.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
        <button onClick={() => setShowForm(!showForm)} style={styles.addButton}>
          {showForm ? 'Cancel' : 'Add Expense'}
        </button>
      </div>

      {showForm && (
        <div style={styles.formContainer}>
          <h2 style={styles.formTitle}>
            {editingExpense ? 'Edit Expense' : 'Add New Expense'}
          </h2>
          <form onSubmit={handleSubmit} style={styles.form}>
            <div style={styles.formRow}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Title:</label>
                <input
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  required
                  style={styles.input}
                />
              </div>
              <div style={styles.formGroup}>
                <label style={styles.label}>Amount:</label>
                <input
                  type="number"
                  name="amount"
                  value={formData.amount}
                  onChange={handleChange}
                  required
                  step="0.01"
                  min="0"
                  style={styles.input}
                />
              </div>
            </div>
            <div style={styles.formRow}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Category:</label>
                <select
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                  style={styles.input}
                >
                  {CATEGORIES.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>
              <div style={styles.formGroup}>
                <label style={styles.label}>Date:</label>
                <input
                  type="date"
                  name="date"
                  value={formData.date}
                  onChange={handleChange}
                  required
                  style={styles.input}
                />
              </div>
            </div>
            <div style={styles.formGroup}>
              <label style={styles.label}>Notes:</label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                rows="3"
                style={styles.textarea}
              />
            </div>
            <div style={styles.formButtons}>
              <button type="submit" style={styles.submitButton}>
                {editingExpense ? 'Update' : 'Add'} Expense
              </button>
              <button type="button" onClick={resetForm} style={styles.cancelButton}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div style={styles.expensesList}>
        {expenses.length === 0 ? (
          <p style={styles.noData}>No expenses found</p>
        ) : (
          expenses.map(expense => (
            <div key={expense.id} style={styles.expenseCard}>
              <div style={styles.expenseHeader}>
                <h3 style={styles.expenseTitle}>{expense.title}</h3>
                <span style={styles.expenseAmount}>${expense.amount.toFixed(2)}</span>
              </div>
              <div style={styles.expenseDetails}>
                <span style={styles.expenseCategory}>{expense.category}</span>
                <span style={styles.expenseDate}>
                  {new Date(expense.date).toLocaleDateString()}
                </span>
              </div>
              {expense.notes && (
                <p style={styles.expenseNotes}>{expense.notes}</p>
              )}
              <div style={styles.expenseActions}>
                <button onClick={() => handleEdit(expense)} style={styles.editButton}>
                  Edit
                </button>
                <button onClick={() => handleDelete(expense.id)} style={styles.deleteButton}>
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
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
  headerButtons: {
    display: 'flex',
    gap: '10px'
  },
  backButton: {
    padding: '10px 20px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px'
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
  controls: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '20px',
    gap: '10px'
  },
  filter: {
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '16px',
    minWidth: '200px'
  },
  addButton: {
    padding: '10px 20px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px'
  },
  formContainer: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    marginBottom: '30px'
  },
  formTitle: {
    margin: '0 0 20px 0',
    color: '#333'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px'
  },
  formRow: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '20px'
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '5px'
  },
  label: {
    fontWeight: 'bold',
    color: '#555'
  },
  input: {
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '16px'
  },
  textarea: {
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '16px',
    fontFamily: 'inherit'
  },
  formButtons: {
    display: 'flex',
    gap: '10px',
    marginTop: '10px'
  },
  submitButton: {
    padding: '12px 24px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px'
  },
  cancelButton: {
    padding: '12px 24px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px'
  },
  expensesList: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '20px'
  },
  expenseCard: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
  },
  expenseHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px'
  },
  expenseTitle: {
    margin: 0,
    fontSize: '18px',
    color: '#333'
  },
  expenseAmount: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#007bff'
  },
  expenseDetails: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '10px',
    color: '#666',
    fontSize: '14px'
  },
  expenseCategory: {
    fontWeight: 'bold'
  },
  expenseDate: {},
  expenseNotes: {
    margin: '0 0 15px 0',
    color: '#666',
    fontSize: '14px',
    fontStyle: 'italic'
  },
  expenseActions: {
    display: 'flex',
    gap: '10px'
  },
  editButton: {
    padding: '8px 16px',
    backgroundColor: '#ffc107',
    color: '#333',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px'
  },
  deleteButton: {
    padding: '8px 16px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px'
  },
  error: {
    backgroundColor: '#f8d7da',
    color: '#721c24',
    padding: '10px',
    borderRadius: '4px',
    marginBottom: '20px',
    textAlign: 'center'
  },
  loading: {
    textAlign: 'center',
    padding: '50px',
    fontSize: '18px',
    color: '#666'
  },
  noData: {
    textAlign: 'center',
    color: '#999',
    fontSize: '18px',
    padding: '50px'
  }
}

export default Expenses
