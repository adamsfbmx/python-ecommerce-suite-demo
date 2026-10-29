# 🛍️ Store — Premium E-Commerce Platform

A complete, production-ready e-commerce platform built with Flask and PostgreSQL.
Designed for fashion and retail businesses that need a modern, multilingual,
and fully-featured online store with an integrated admin panel.

## ✨ Features

### Storefront
- 🎨 Premium, responsive design
- 🌍 **Multilingual** (English, Spanish, French, Italian)
- 🔍 Live product search
- 👕 Product filtering by gender
- 🛒 Shopping cart with session persistence
- 🎟️ Coupon code support
- ⭐ Verified customer reviews
- 📸 Multiple product images (gallery)
- 🎯 Variable products (size + color + stock per variant)

### Checkout & Payments
- 💳 **Stripe** integration (cards)
- 🅿️ **PayPal** integration
- 💵 **Cash on Delivery**
- 🏦 **Bank Transfer**
- 📧 Automatic order confirmation emails

### Customer Accounts
- 📝 Registration with email verification
- 🔐 Login / logout / password reset
- 📦 Order history ("My Orders")
- 👤 Session-based authentication

### Admin Panel (`/admin`)
- 📊 Financial dashboard
- 📦 Product management (create, edit, delete)
- 🎨 Category management
- 📋 Order management (status updates)
- 👥 Customer list
- ⚙️ Store settings (payment gateways, SMTP)
- 📈 Accounting reports (printable)

## 🚀 Quick Start

```bash
tar -xzf store_delivery.tar.gz
cd store_delivery
sudo chmod +x install.sh
sudo ./install.sh
