'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { apiClient } from '@/lib/apiClient';
import { useUserStore } from '@/lib/useUserStore';
import { showErrorToast } from '@/lib/utils';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { toast } = useToast();

  const setUserInfo = useUserStore((s) => s.setUserInfo);
  const setPersonId = useUserStore((s) => s.setPersonId);
  const setIsLoggedIn = useUserStore((s) => s.setIsLoggedIn);
  const clearUser = useUserStore((s) => s.clear);
  const initUser = useUserStore((s) => s.init);

  // 在页面加载时清除全局状态
  useEffect(() => {
    clearUser();
    console.log('已清除登录状态和用户信息');
  }, [clearUser]);

  // 处理登录
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // 调用登录API
    const loginResponse = await apiClient.login(username, password);
    if (loginResponse.code === 200) {
      // 获取用户信息
      const userInfoResp = await apiClient.getUserInfo(username);
      if (userInfoResp.code === 200) {
        initUser({
          userInfo: userInfoResp.data.info,
          personId: userInfoResp.data.person_id,
          isLoggedIn: true
        });
        toast({
          title: '登录成功',
          description: `欢迎回来，${username}，正在跳转到个人档案页面...`,
        });
        setTimeout(() => {
          router.push('/profile');
        }, 1000);
      } else {
        showErrorToast(toast, userInfoResp);
      }
    } else {
      showErrorToast(toast, loginResponse);
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 p-4">
      <div className="w-full max-w-md">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Card className="glass-effect">
            <CardHeader className="space-y-1">
              <CardTitle className="text-2xl text-center font-bold">"AI+” 档案管理</CardTitle>
              <CardDescription className="text-center">请输入您的账号和密码登录系统</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleLogin} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="username">用户名</Label>
                  <Input 
                    id="username" 
                    placeholder="请输入用户名" 
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="password">密码</Label>
                  <Input 
                    id="password" 
                    type="password" 
                    placeholder="请输入密码" 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                <Button 
                  type="submit" 
                  className="w-full" 
                  disabled={isLoading}
                  variant="gradient"
                >
                  {isLoading ? '登录中...' : '登录'}
                </Button>
              </form>
            </CardContent>
            <CardFooter>
              <p className="text-xs text-center w-full text-muted-foreground">
                提示：用户名 lisi，密码 password
              </p>
            </CardFooter>
          </Card>
        </motion.div>
        
        {/* 装饰元素 */}
        <motion.div 
          className="absolute top-10 right-10 w-20 h-20 rounded-full bg-blue-500 opacity-20"
          animate={{ 
            scale: [1, 1.2, 1],
            rotate: [0, 90, 0],
          }}
          transition={{ 
            duration: 8, 
            repeat: Infinity,
            ease: "easeInOut" 
          }}
        />
        <motion.div 
          className="absolute bottom-10 left-10 w-32 h-32 rounded-full bg-indigo-500 opacity-20"
          animate={{ 
            scale: [1, 1.3, 1],
            rotate: [0, -90, 0],
          }}
          transition={{ 
            duration: 10, 
            repeat: Infinity,
            ease: "easeInOut" 
          }}
        />
      </div>
    </div>
  );
}