# Blockchain Web Interface

This is a simple web interface for interacting with your blockchain application, replicating the functionality of `test.py`.

## Setup

1. Ensure your blockchain (e.g., Ganache) is running on `http://127.0.0.1:7546`
2. Install dependencies: `pip install flask web3`
3. Run the app: `python app.py`

## Default Admin Account

- **Username:** `admin`
- **Password:** `0x5B38Da6a701c568545dCfcB03FcB875f56beddC4` (contract address)

## Usage

1. Open your browser and go to `http://127.0.0.1:5000`
2. Enter the RPC URL (default is `http://127.0.0.1:7546`)
3. Click "Connect" to connect to the blockchain
4. Select your role: User or Admin
5. For Admin role, enter the contract address
6. Use the various buttons to perform actions

## Features

### User Functions
- Check ETH balance of an address
- View all account balances

### Admin Functions
- All user functions
- **Integrated Enhanced User Management Dashboard** (directly in admin mode)
- View contract owner
- Transfer ownership
- Mint tokens
- Burn tokens
- Transfer tokens
- Send ETH
- Check token balance
- View past token transfers
- View contract information

### Enhanced Admin Panel Features (Integrated in Main Interface)
When logged in as admin and in Admin Mode:

#### 📊 Dashboard Statistics
- **Real-time Stats**: Live counts of pending, approved, and total users
- **Visual Indicators**: Color-coded statistics cards with modern design

#### 👥 Advanced User Management
- **Approve User Button**: Dedicated button that opens the full admin panel page for user approval
- **Load Pending Users**: View all users awaiting approval with detailed information
- **View Approved Users**: See all approved user accounts with role information
- **Approve/Reject Users**: One-click actions with loading states and confirmations
- **Real-time Updates**: Instant refresh without page reload

#### 🔍 Search & Filter
- **Search Functionality**: Find users by username with live filtering
- **Role Filtering**: Filter users by role (All, User, Admin)
- **Instant Results**: Real-time filtering as you type

#### 🎨 Enhanced UI/UX
- **Modern Design**: Glass-morphism effects, gradients, and smooth animations
- **User Avatars**: Colorful avatar circles with user initials
- **Status Badges**: Visual status indicators for pending/approved users
- **Responsive Layout**: Fully responsive design for mobile and desktop
- **Loading States**: Visual feedback during API calls
- **Toast Notifications**: Non-intrusive success/error messages
- **Hover Effects**: Interactive elements with smooth transitions

#### 📱 Mobile Responsive
- **Adaptive Layout**: Optimized for all screen sizes
- **Touch-Friendly**: Large buttons and touch targets
- **Flexible Grid**: Responsive user lists and statistics

### Dedicated Admin Panel Page
- **Separate Admin Interface**: Click "Approve User" button to access dedicated admin.html page
- **Full-Featured User Management**: Complete user approval workflow in dedicated interface
- **Enhanced Admin Experience**: Professional admin panel with comprehensive user management tools

### User Interface Highlights
- **Glass-morphism Design**: Modern translucent panels with backdrop blur
- **Gradient Buttons**: Beautiful gradient buttons with hover animations
- **Card-based Layout**: Clean card design for user information
- **Smooth Animations**: CSS transitions for all interactive elements
- **Professional Typography**: Clean, readable fonts with proper hierarchy
- **Color-coded Actions**: Green for approve, red for reject, blue for primary actions

**Note**: The admin panel is now fully integrated into the main blockchain interface with enterprise-level UI/UX design. Admins can manage users seamlessly without leaving the application context.