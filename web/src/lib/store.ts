'use client';

// 定义事件名称
const USER_INFO_CHANGE_EVENT = 'user-info-change';

// 创建自定义事件，用于通知状态变化
const createChangeEvent = () => {
  return new CustomEvent(USER_INFO_CHANGE_EVENT);
};

// 用户信息存储和管理
export const userStore = {
  // 设置用户信息
  setUserInfo: (userInfo: any) => {
    // 存储到localStorage
    localStorage.setItem('userInfo', JSON.stringify(userInfo));
    // 触发变更事件
    window.dispatchEvent(createChangeEvent());
  },

  // 获取用户信息
  getUserInfo: (): any | null => {
    const userInfoStr = localStorage.getItem('userInfo');
    if (!userInfoStr) return null;
    
    try {
      return JSON.parse(userInfoStr);
    } catch (error) {
      console.error('解析用户信息失败:', error);
      return null;
    }
  },

  // 清除用户信息
  clearUserInfo: () => {
    localStorage.removeItem('userInfo');
    localStorage.removeItem('person_id');
    localStorage.removeItem('isLoggedIn');
    window.dispatchEvent(createChangeEvent());
  },

  // 订阅用户信息变化
  subscribe: (callback: () => void) => {
    window.addEventListener(USER_INFO_CHANGE_EVENT, callback);
    return () => {
      window.removeEventListener(USER_INFO_CHANGE_EVENT, callback);
    };
  }
};


