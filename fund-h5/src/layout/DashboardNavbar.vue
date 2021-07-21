<template>
  <base-nav
    class="navbar-top navbar-dark"
    id="navbar-main"
    :show-toggle-button="false"
    expand
  >
    <form
      class="
        navbar-search navbar-search-dark
        form-inline
        mr-3
        d-none d-md-flex
        ml-lg-auto
      "
    >
      <div class="form-group mb-0">
        <base-input
          placeholder="Search"
          class="input-group-alternative"
          alternative=""
          addon-right-icon="fas fa-search"
          
          @click="clicksearch"
        >
        </base-input>
      </div>
    </form>
    <ul class="navbar-nav align-items-center d-none d-md-flex">
      <li class="nav-item dropdown">
        <base-dropdown class="nav-link pr-0">
          <template v-slot:title>
            <div class="media align-items-center">
              <span class="avatar avatar-sm rounded-circle">
                <img
                  alt="Image placeholder"
                  src="img/theme/team-4-800x800.jpg"
                />
              </span>
              <div class="media-body ml-2 d-none d-lg-block">
                <span class="mb-0 text-sm font-weight-bold">Jessica Jones</span>
              </div>
            </div>
          </template>
          <div class="dropdown-header noti-title">
            <h6 class="text-overflow m-0">Welcome!</h6>
          </div>
          <router-link to="/profile" class="dropdown-item">
            <i class="ni ni-single-02"></i>
            <span>My profile</span>
          </router-link>
          <router-link to="/profile" class="dropdown-item">
            <i class="ni ni-settings-gear-65"></i>
            <span>Settings</span>
          </router-link>
          <router-link to="/profile" class="dropdown-item">
            <i class="ni ni-calendar-grid-58"></i>
            <span>Activity</span>
          </router-link>
          <router-link to="/profile" class="dropdown-item">
            <i class="ni ni-support-16"></i>
            <span>Support</span>
          </router-link>
          <div class="dropdown-divider"></div>
          <router-link to="/profile" class="dropdown-item">
            <i class="ni ni-user-run"></i>
            <span>Logout</span>
          </router-link>
        </base-dropdown>
      </li>
    </ul>
    <!-- 搜索框弹出 -->
    <div
      class="mask-s"
      v-if="isShowSearch == false"
      @click="isShowSearch = true"
    />
    <div class="container-s" v-if="isShowSearch == false">
      <div class="form-container-s">
        <div class="form-tab-s">
          <div class="search-field-s">
            <i data-feather="search" class="search-icon-s"></i>
            <p class="search-placeholder-s">搜索你要的基金</p>
            <form>
              <input
                autocomplete="off"
                type="text"
                pattern="\S+.*"
                name="input"
                id="input"
                class="text-field-s"
                v-model="searchcontent"
                @keyup="getsearch"
              />
            </form>
          </div>
          <div class="search-btn-s">
            <p>search</p>
          </div>
        </div>
      </div>
      <div class="resoult-tab-s">
        <!-- <div class="ul-title-s">
          <p>Recent Search</p>
        </div> -->
        <div class="ul-s" v-for="item in searchResult" :key="item.id">
          <!-- 查询的结果 -->
          <div class="li-s li-1-s">
            <div class="li-icon-s">
              <i data-feather="clipboard" class="icon-s"></i>
            </div>
            <div class="li-text-s">{{item.fundcode}}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
            <div class="li-text-s">{{item.fundname}}</div>
          </div>
          
        </div>
      </div>
    </div>
    <!-- ------- -->
  </base-nav>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      activeNotifications: false,
      showMenu: false,
      searchResult: [],
      isShowSearch: true,
      searchcontent:''
      
    };
  },
  methods: {
    clicksearch() {
      this.isShowSearch = !this.isShowSearch;
      setTimeout(() => {
        const searchInput = document.getElementById("input");
        searchInput.addEventListener("focus", () => {
          const resoultTab = document.getElementsByClassName("resoult-tab-s")[0];
          resoultTab.className += " resoult-tab-active-s";
          console.log(resoultTab,resoultTab.class);
          setTimeout(()=>{
            document.getElementsByClassName("ul-title-s")[0].style.opacity = 1;
          }, 299);
          // List fade in
          setTimeout(()=>{
            document.getElementsByClassName("li-s")[0].className +=" li-active";
          }, 0);
        });
        searchInput.addEventListener("blur", () => {
          // const resoultTab = document.getElementByClassName("resoult-tab-s")[0];
        });
        searchInput.focus();
      }, 300);
      console.log(this.isShowSearch);
    },
    getsearch() {
      axios({
        url: "http://localhost:8000/queryfundtocode/",
        method: "get",
        params: {
          fundcode: this.searchcontent,
        },
      }).then((response) => {
        // console.log(response);
        this.searchResult = response.data.data.infos;
        console.log(this.searchResult)
      }),
        (err) => {
          console.log(err);
        };
    },
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    hideSidebar() {
      this.$sidebar.displaySidebar(false);
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    search(event){
      console.log(event)
    }
  },
};
</script>
