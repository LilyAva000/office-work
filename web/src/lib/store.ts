'use client';

// 定义事件名称
const USER_INFO_CHANGE_EVENT = 'user-info-change';

// 创建自定义事件，用于通知状态变化
const createChangeEvent = () => {
  return new CustomEvent(USER_INFO_CHANGE_EVENT);
};

// 集中管理所有key和localStorage字段映射及序列化规则
const USER_STORE_META = {
  userInfo: {
    storageKey: 'userInfo',
    serialize: (v: any) => JSON.stringify(v),
    deserialize: (v: string | null) => {
      if (!v) return null;
      try { return JSON.parse(v); } catch { return null; }
    }
  },
  personId: {
    storageKey: 'personId',
    serialize: (v: any) => v,
    deserialize: (v: string | null) => v
  },
  isLoggedIn: {
    storageKey: 'isLoggedIn',
    serialize: (v: any) => v ? 'true' : 'false',
    deserialize: (v: string | null) => v === 'true'
  }
} as const;
type UserStoreKey = keyof typeof USER_STORE_META;

// 用户信息存储和管理
export const userStore = {
  // 通用设置
  set: (key: UserStoreKey, value: any) => {
    const meta = USER_STORE_META[key];
    if (!meta) {
      console.error(`[userStore] set: 不存在的key: ${key}`);
      return;
    }
    localStorage.setItem(meta.storageKey, meta.serialize(value));
    window.dispatchEvent(createChangeEvent());
  },
  // 通用获取
  get: (key: UserStoreKey) => {
    const meta = USER_STORE_META[key];
    if (!meta) {
      console.error(`[userStore] get: 不存在的key: ${key}`);
      return null;
    }
    return meta.deserialize(localStorage.getItem(meta.storageKey));
  },
  // 一次性初始化所有
  init: (data: { userInfo: any; personId: string; isLoggedIn: boolean }) => {
    (Object.keys(USER_STORE_META) as UserStoreKey[]).forEach(key => {
      // @ts-ignore
      userStore.set(key, data[key]);
    });
    window.dispatchEvent(createChangeEvent());
  },
  // 一次性清空所有
  clear: () => {
    Object.values(USER_STORE_META).forEach(meta => localStorage.removeItem(meta.storageKey));
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


