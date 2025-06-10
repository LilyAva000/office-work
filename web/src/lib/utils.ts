import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// 公共错误toast工具函数，所有页面可直接import使用
export function showErrorToast(toast: any, response: { code: number; msg: string; data?: any }) {
  toast({
    title: `错误码: ${response.code}`,
    description: `${response.msg}${response.data ? '：' + response.data : ''}`,
    variant: 'destructive',
  });
}
