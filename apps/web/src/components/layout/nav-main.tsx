'use client';

import { CalendarRange, Globe, LayoutDashboard, TrendingUp } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
	SidebarGroup,
	SidebarGroupLabel,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
	useSidebar,
} from '@/components/ui/sidebar';

const items = [
	{ title: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
	{ title: 'Upcoming Fights', href: '/upcoming', icon: CalendarRange },
	{ title: 'Predictions', href: '/predictions', icon: TrendingUp },
	{ title: 'Browser', href: '/browser', icon: Globe },
];

export function NavMain() {
	const pathname = usePathname();
	const { setOpenMobile } = useSidebar();

	return (
		<SidebarGroup>
			<SidebarGroupLabel>Navigation</SidebarGroupLabel>
			<SidebarMenu>
				{items.map((item) => (
					<SidebarMenuItem key={item.href}>
						<SidebarMenuButton
							asChild
							isActive={pathname === item.href}
							onClick={() => setOpenMobile(false)}
						>
							<Link href={item.href}>
								<item.icon />
								<span>{item.title}</span>
							</Link>
						</SidebarMenuButton>
					</SidebarMenuItem>
				))}
			</SidebarMenu>
		</SidebarGroup>
	);
}
