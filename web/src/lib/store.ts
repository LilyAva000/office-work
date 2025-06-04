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

// 注意！！路径中/的拼接，多余的/会导致请求失败
const BASE_URL = 'http://127.0.0.1:8008';
const API_BASE_URL = BASE_URL + '/api';

// API请求工具
export const apiClient = {
  BASE_URL,
  API_BASE_URL,
  
  // 登录方法
  login: async (username: string, password: string): Promise<any> => {
    const response = await fetch(`${apiClient.API_BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        password
      }),
    });
    
    if (!response.ok) {
      throw new Error(`登录失败: ${response.status}`);
    }
    
    return await response.json();
  },

  // 获取用户信息
  getUserInfo: async (username: string): Promise<any> => {
    const response = await fetch(`${apiClient.API_BASE_URL}/info/${username}`);
    
    if (!response.ok) {
      throw new Error(`获取用户信息失败: ${response.status}`);
    }

    const res = await response.json();
    if (res.status === 200) {
      return res.data;
    } else {
      throw new Error(res.message || '获取用户信息失败');
    }
  },
  
  // 更新用户信息
  updateUserInfo: async (username: string, userInfo: any): Promise<any> => {
    const response = await fetch(`${apiClient.API_BASE_URL}/info/${username}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        person_info: userInfo
      }),
    });
    
    if (!response.ok) {
      throw new Error(`更新用户信息失败: ${response.status}`);
    }
    
    return await response.json();
  },
  
  // 上传头像
  uploadAvatar: async (username: string, file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('file', file);
    const response = await fetch(`${apiClient.API_BASE_URL}/upload_avatar`, {
      method: 'POST',
      body: formData,
    });
    const result = await response.json();
    if (result.status === 200 && result.avatar) {
      return result;
    } else {
      throw new Error(result.detail || '头像上传失败');
    }
  },
  
  // 可以添加更多API请求方法
};