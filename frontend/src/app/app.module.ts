import { NgModule } from '@angular/core'
import { StoreModule } from '@ngrx/store'
import { EffectsModule } from '@ngrx/effects'
import { SharedModule } from '@/shared/shared.module'
import { LayoutModule } from '@/layout/layout.module'
import { AuthModule } from '@/auth/auth.module'
import { ContestsModule } from '@/contests/contests.module'
import { AppRoutingModule } from '@/app-routing.module'
import { AppComponent } from '@/app.component'
import { UsersService } from '@api/users/users.service'
import { NewsModule } from '@/news/news.module'
import { ChatModule } from '@/chat/chat.module'
import { AuthGuardService } from '@/shared/auth.guard.service'
import { TasksService } from '@api/tasks/tasks.service'
import { ResponsesService } from '@api/responses/responses.service'
import { ProfileModule } from '@/profile/profile.module'
import { RootEffects } from '@/app.effects'
import { ManageUsersModule } from '@/manage-users/manage-users.module'
import { ManageContestsModule } from '@/manage-contests/manage-contests.module'
import { AdminAuthGuardService } from '@/shared/admin.auth.guard.service'


const COMMON_MODULES = [
    SharedModule,
    LayoutModule,
    AuthModule
]

const PARTICIPANT_MODULES = [
    ContestsModule,
    ProfileModule
]

const ADMIN_MODULES = [
    ManageUsersModule,
    ManageContestsModule
]


@NgModule( {
    declarations: [ AppComponent ],
    imports: [
        ...COMMON_MODULES,
        ...PARTICIPANT_MODULES,
        ...ADMIN_MODULES,
        AppRoutingModule,
        StoreModule.forRoot( {} ),
        EffectsModule.forRoot( [ RootEffects ] )
    ],
    providers: [
        { provide: UsersService },
        { provide: TasksService },
        { provide: ResponsesService },
        { provide: AuthGuardService },
        { provide: AdminAuthGuardService }
    ],
    bootstrap: [ AppComponent ]
} )
export class AppModule {}