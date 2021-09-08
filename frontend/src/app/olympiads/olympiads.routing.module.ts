import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { AuthGuardService } from '@/shared/auth.guard.service'
import { HomeComponent } from '@/olympiads/containers/home/home.component'


const routes: Routes = [
    {
        path: '',
        children: [
            {
                path: 'user', component: HomeComponent, canActivate: [ AuthGuardService ]
            }
        ]
    }
]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class OlympiadsRoutingModule {}