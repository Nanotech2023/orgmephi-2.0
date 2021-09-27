import { NgModule } from '@angular/core'
import { StoreModule } from '@ngrx/store'
import { EffectsModule } from '@ngrx/effects'
import { StoreDevtoolsModule } from '@ngrx/store-devtools'
import { SharedModule } from '@/shared/shared.module'
import { LayoutModule } from '@/layout/layout.module'
import { AuthModule } from '@/auth/auth.module'
import { ContestsModule } from '@/contests/contests.module'
import { AppRoutingModule } from '@/app-routing.module'
import { environment } from '@environments/environment'
import { AppComponent } from '@/app.component'
import { UsersService } from '@api/users/users.service'
import { ManageContestsModule } from '@/manage-contests/manage-contests.module'
import { ManageUsersModule } from '@/manage-users/manage-users.module'
import { AuthGuardService } from '@/shared/auth.guard.service'
import { TasksService } from '@api/tasks/tasks.service'
import { ResponsesService } from '@api/responses/responses.service'


@NgModule( {
    declarations: [
        AppComponent
    ],
    imports: [
        SharedModule,
        LayoutModule,
        AuthModule,
        ContestsModule,
        // TODO fix profile module
        // ProfileModule,
        ManageUsersModule,
        ManageContestsModule,
        AppRoutingModule,
        StoreModule.forRoot( {} ),
        EffectsModule.forRoot( [] ),
        environment.production ? [] : StoreDevtoolsModule.instrument()
    ],
    providers: [
        { provide: UsersService },
        { provide: TasksService },
        { provide: ResponsesService },
        { provide: AuthGuardService }
    ],
    bootstrap: [ AppComponent ]
} )
export class AppModule {}